# `TDTU-Information-Technology-Project`

## Table of Contents
1. [Installation & Setup](#1-installation--setup)
2. [Data and Preprocessing](#2-data-collection-and-preprocessing)
3. [Convolutional Models and Feature Maps](#3-convonlutional-models-and-extraction-feature-maps)
4. [Clustering and Distance Vectors](#4-clustering-and-computation-distance-vectors)
5. [Classification with Distance Vectors](#5-classification-models-trained-with-distance-vectors)
6. [Classification with Direct Feature Maps](#6-classifcation-models-trained-with-feature-maps-directly)

## 1 Installation & Setup
Ensure that all dependencies required for connection handling are installed before using this module.

```python
pip install -r requirements.txt
```

## 2 Data collection and Preprocessing
The project operates on multiple sources of data:

Raw data is available under the dataset-raw directory.
Filtered datasets can be found in dataset-filter.
Additional data manipulation and collection scripts reside in the [data collection](./data-collection/).
Feature maps and distance vectors are stored in the feature_maps and distance_vectors directories respectively.
Ensure that data is properly preprocessed before training, as outlined in the respective directories.

## 3 Convonlutional Models and extraction feature maps
The [Cnn models](./cnn) implemented in this repository are designed to extract deep feature maps for further processing. You can review the implementation details in the cnn models directory.

## 4 Clustering and computation distance vectors
[Clustering models](./clustering/) process the extracted feature maps to compute distance vectors which are then used for further classification. For exploration, check out the clustering models folder.

## 5 Classification models trained with distance vectors
[Classification model](./classification_model/) trained on distance vectors provide a method for categorizing inputs based on computed similarities. The relevant models are located in Classification model.

## 6 Classifcation models trained with feature maps directly
[Classification models](./classification_model_trained_feature_maps/) - An alternative approach leverages the direct use of feature maps in training classification models. The implementations can be found in Classification models.