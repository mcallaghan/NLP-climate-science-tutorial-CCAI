This repository contains materials for a tutorial on using NLP in research synthesis in the field of climate change. The following gives an outline of the tutorial.

# Synopsis

Understanding climate change, and developing climate solutions, is predicated on our collective understanding of complex physical, biological, and social systems and their interplay. The scientific literature about climate change comprises hundreds of thousands of articles across disciplines, and to advance our knowledge of climate change, we need to be able to learn from these studies by synthesising the literature. This is done at a grand scale in global environmental assessments like the IPCC - whose assessment of the science of climate change are vital inputs into international climate policy - as well as in individual evidence synthesis projects like systematic maps and reviews. Producing evidence synthesis that is systematic, i.e. transparent about the selection of studies, and as comprehensive as is feasible, is challenged by the amount of literature published. In this tutorial we will explore how Natural Language Processing (NLP) can be used to assist in identifying and mapping climate-relevant literature.

# Learning objectives

During the course of the tutorial participants will gain an understanding of the broad range of ways that NLP can assist research synthesis. In particular you will gain hands on experience replicating an ML-assisted evidence map of climate impacts research, learning the following skills

- Obtaining abstracts and meta-data from research studies by searching bibliographic databases
- Using supervised learning to replicate human annotations of studies
- Choosing hyperparameters and evaluating models
- Mapping research

# Schedule

## Introduction to "Big Literature" and machine-learning assisted evidence synthesis
- Describe what the IPCC does, how this fits into broader concept of evidence synthesis
- Describe how the growth of the literature on climate change implies challenges for IPCC and synthetic research
- Describe traditional methods and questions within evidence synthesis
- Show how machine-learning can be used to help
  - topic modelling for exploration
  - researcher-in-the-loop methods to identify relevant literature faster
  - machine-learning assisted maps with supervised learning

## Practical part 1: Obtaining research metadata
- Get data from OpenAlex database using API
- Basic exploratory data analysis of research dataset

## Practical part 2: Learning from human annotations
- Merge with human annotations (here are some we made earlier)
- Demonstrate nested cross-validation strategy (draw graph)
- Train and validate, and make predictions with "Relevance" classifier (binary)
- Train and validate, and make predictions with "impact type" classifier (multilabel)


## Practical part 2.2: Geoparsing  
- Extract place names using mordecai
- Resolve places to grid cells (probably leave this out)

## Practical part 3: Mapping and visualisation
- Plot results:
  - heatmaps
  - graphs with numbers by impact type and region and over time
  - maps
