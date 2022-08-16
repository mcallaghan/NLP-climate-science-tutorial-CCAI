# Conclusion

To recap, in this tutorial we have learned

- how to get bibliographic data from the Open Source database OpenAlex
- How to set up simple machine learning pipelines for texts using Support vector machines with `scikitlearn`
- How to classify texts by fine-tuning language models from `transformers`
- How to evaluate models and choose hyperparameters
- How to extract structured geographical information from texts and plot this on a grid cell level.


### What is this useful for?

The number of scientific publications on climate change has reached levels where traditional methods of synthesis are 
challenging. Using machine learning, we are able to more efficiently identify and classify relevant literature.

This work of identification and classification is similar in nature to the production of [systematic maps](https://environmentalevidencejournal.biomedcentral.com/articles/10.1186/s13750-016-0059-6).
These can be used to identify where we have lots of evidence, or where we have evidence gaps, and the maps can provide starting
points towards more detailed systematic reviews.

It is important to note that machine learning is a **complement** - not a **substitute** - for expert knowledge. 
We could not, and indeed would not want to, automate the process of the IPCC. 
However given scarce resources and the massive task of keeping on top of climate science literature, 
it does make sense to use machine learning in order to deploy those resources more effectively. 
Especially if it means we can

- Assess a wider pool of evidence
- Be as transparent about the selection process (from query to model performance) as possible
- Update this efficiently

It is important to remember, we are already "using" machine learning when we search for studies in google scholar.

## Some more things to try

Using NLP to look at scientific texts is a large research area, and there are many other things we can try.

#### Unsupervised learning

Where we do not have a specific set of categories into which we want to classify documents, we may find it interesting to use **unsupervised learning** to classify studies. 
Some examples in climate literature are on [climate and health](https://apsis.mcc-berlin.net/climate-health/), 
and on [the literature as a whole](https://www.nature.com/articles/s41558-019-0684-5).

#### Researcher in the Loop for systematic reviews

Instead of simply screening documents and then making predictions, we can use prediction in order to prioritise which documents we screen.
This process is sometimes called "researcher in the loop": 
[link](https://www.nature.com/articles/s42256-020-00287-7), 
[link](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/2046-4053-4-5).
However, it is important to think more carefully about [stopping criteria](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-020-01521-4) than has often been done when presenting such systems

