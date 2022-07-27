# First we need to load the data
import argparse
import pandas as pd
import numpy as np
import re
import random
import os
import json
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import ParameterGrid, KFold
from sklearn.metrics import f1_score, recall_score, precision_score


def load_data(test):
    labelled_data = pd.read_csv("data/labelled_data.csv")

    # We create a lower case version of the title without spaces and punctuation, to allow for merging
    labelled_data["title_lcase"] = labelled_data["title"].apply(lambda x: re.sub(r"\W", "", x).lower())
    # We also want to get rid of documents without abstracts, as we can't use these for learning
    labelled_data = labelled_data.dropna(subset=["abstract"])

    # Now we load the Open alex data, and create the same title variable for merging

    oa_data = pd.read_csv("data/openalex_data.csv").rename(columns={"id": "OA_id"})
    oa_data["title_lcase"] = oa_data["title"].apply(lambda x: re.sub(r"\W", "", x).lower())

    # Get only those rows which don't match the labels
    oa_data = oa_data[~oa_data["title_lcase"].isin(labelled_data["title_lcase"])]
    oa_data = oa_data.dropna(subset=["abstract"])  # Drop rows without abstracts
    oa_data["seen"] = 0

    if test:
        labelled_data = labelled_data.sample(500)  # just take a sample of each
        oa_data = oa_data.sample(100)

    # Now we add the OpenAlex rows which are not in the labelled data to the labelled_data
    df = pd.concat([
        labelled_data,
        oa_data
    ]).sample(frac=1).reset_index(drop=True)
    return df


def fit_eval_model(pipeline, param_set, x, y, train_index, val_index, metrics):
    clf = pipeline.set_params(**param_set)
    clf.fit(x[train_index], y[train_index])
    y_pred = clf.predict(x[val_index])
    if y.ndim==1:
        scores = {metric.__name__: metric(y[val_index], y_pred) for metric in metrics}
    elif y.ndim==2: # For multilabel we need to evaluate differently
        scores = {}
        for metric in metrics:
            for average in ["micro", "macro", "weighted"]: # We can get different types of average scores
                scores[f"{metric.__name__}_{average}"] = metric(y[val_index], y_pred, average=average)
            for c in np.arange(y.shape[1]): # And we can also calculate each score for each class
                scores[f"{metric.__name__}_{c}"] = metric(y[val_index,c], y_pred[:,c])
    return scores


def get_best_param(scores, scorer):
    return (pd.DataFrame(scores)
        .groupby("param_id")[scorer]
        .mean()
        .sort_values(ascending=False).index[0]
    )


def main(y_prefix, n_splits, test):
    # Get our data
    df = load_data(test)

    X = df["abstract"].values
    cols = [x for x in df.columns if re.match(f"^{y_prefix}", x)]
    if len(cols)==1:
        cols = cols[0]
        # We need to use a pipeline for a binary classifier
        pipeline = Pipeline(steps=[
            ("vect", TfidfVectorizer()),
            ("clf", SVC(probability=True, class_weight="balanced"))
        ])
        # And we'll get our binary parameter space
        with open("parameter_space.json", "r") as fp:
            parameters = json.load(fp)
        # We'll rank models by the simple f1 score
        scorer = "f1_score"
        # For these purposes all documents that have been labelled at all are counted as labelled
        labelled_index = df[df["seen"] == 1].index
    elif len(cols)==0:
        print("Not enough columns match the given y_prefix, exiting...")
        return 1
    else:
        # In a multilabel setting we have a slightly different pipeline
        pipeline = Pipeline(steps=[
            ("vect", TfidfVectorizer()),
            ("clf", OneVsRestClassifier(SVC(probability=True, class_weight="balanced")))
        ])
        # And a slightly differently defined parameter space
        with open("parameter_space_multilabel.json", "r") as fp:
            parameters = json.load(fp)
        # Here we'll rank scores by the macro f1 score
        scorer = "f1_score_macro"
        # In this setting only those labelled documents which were marked as INCLUDE are considered
        labelled_index = df[df["INCLUDE"] == 1].index

    unlabelled_index = df[df["seen"] == 0].index
    y = df[cols].values



    # Create a directory to store our results if it does not already exist, and change into it if it does
    data_path = f"cv_data/{y_prefix}"
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    os.chdir(data_path)

    parameter_combinations = list(ParameterGrid(parameters))
    if test:
        parameter_combinations = random.choices(parameter_combinations, k=5)

    with open("parameter_combinations.json", "w") as fp:
        json.dump(parameter_combinations, fp)

    metrics = [f1_score, precision_score, recall_score]

    ######################################
    # Now we can start the cv experiments

    inner_fold = KFold(n_splits=n_splits)
    outer_fold = KFold(n_splits=n_splits)

    outer_results = []
    outer_search_results = []

    # Do the nested loop

    for i, (o_train_index, test_index) in enumerate(outer_fold.split(labelled_index)):
        #########################
        # TUNE PARAMETERS
        inner_results = []
        for j, (i_train_index, i_val_index) in enumerate(inner_fold.split(o_train_index)):
            for k, param_set in enumerate(parameter_combinations):
                scores = fit_eval_model(
                    pipeline, param_set, X[labelled_index[o_train_index]], y[labelled_index[o_train_index]],
                    i_train_index, i_val_index, metrics
                )
                scores["param_id"] = k
                inner_results.append(scores)

        with open(f"inner_results_{i}_from_{n_splits}_splits.json", "w") as fp:
            json.dump(inner_results, fp, indent=2)

        #######################
        # EVALUATE MODELS
        # fit a model with the best parameters on inner cv, and get the score
        best_param_id = get_best_param(inner_results, scorer)
        scores = fit_eval_model(
            pipeline, parameter_combinations[best_param_id], X[labelled_index], y[labelled_index],
            o_train_index, test_index, metrics
        )
        outer_results.append(scores)

        ######################
        # SEARCH PARAMETERS
        # Now do parameter search on the outer data
        for k, param_set in enumerate(parameter_combinations):
            scores = fit_eval_model(
                pipeline, param_set, X[labelled_index], y[labelled_index],
                o_train_index, test_index, metrics
            )
            scores["param_id"] = k
            outer_search_results.append(scores)

    with open(f"outer_results_{n_splits}_splits.json", "w") as fp:
        json.dump(outer_results, fp, indent=2)

    with open(f"outer_param_search_{n_splits}_splits.json", "w") as fp:
        json.dump(outer_results, fp, indent=2)

    ######################
    # MAKE PREDICTIONS
    # Get parameter_id with best results
    best_param_id = get_best_param(outer_search_results, scorer)
    clf = pipeline.set_params(**parameter_combinations[best_param_id])
    clf.fit(X[labelled_index],  y[labelled_index])

    # These are our final results!
    y_pred = clf.predict_proba(X[unlabelled_index])
    df = pd.DataFrame.from_dict({"OA_id": df.iloc[unlabelled_index]["OA_id"], "prediction": y_pred[:,1]})
    df.to_csv(f"predictions_{n_splits}_splits.csv", index=False)
    return "Success! Tuned parameters, evaluated our models and made predictions"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a cross validation experiment on our labelled data")
    parser.add_argument(
        "y_prefix", type=str,
        help="Variables in the data starting with this prefix will become our target variable"
    )
    parser.add_argument(
        "n_splits", type=int,
    )
    parser.add_argument(
        "--test", action=argparse.BooleanOptionalAction
    )
    args = parser.parse_args()
    main(args.y_prefix, args.n_splits, args.test)
