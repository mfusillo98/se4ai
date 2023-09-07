---

---






# Model Card for VGG16 without last dense layer

<!-- Provide a quick summary of what the model is/does. [Optional] -->
It uses a powerful image model called VGG16 to extract features from images, unique characteristics that describe each image. 
PCA is used to choose the most important features, is useful for quickly analyzing images and finding the most important aspects.




#  Table of Contents

- [Model Card for MODEL CARD: VGG16 without last dense layer](#model-card-for--model_id-)
- [Model Details](#model-details)
  - [Model Description](#model-description)
- [Uses](#uses)
  - [Downstream Use](#downstream-use-optional)
  - [Out-of-Scope Use](#out-of-scope-use)
- [Bias, Risks, and Limitations](#bias-risks-and-limitations)
  - [Recommendations](#recommendations)
- [Training Details](#training-details)
  - [Training Data](#training-data)
  - [Training Procedure](#training-procedure)
    - [Preprocessing](#preprocessing)
    - [Speeds, Sizes, Times](#speeds-sizes-times)
- [Evaluation](#evaluation)
  - [Testing Data, Factors & Metrics](#testing-data-factors--metrics)
    - [Testing Data](#testing-data)
    - [Factors](#factors)
    - [Metrics](#metrics)
  - [Results](#results)
- [Model Examination](#model-examination)
  - [Model Architecture and Objective](#model-architecture-and-objective)
- [Citation](#citation)
- [Model Card Authors](#model-card-authors-optional)


# Model Details

## Model Description

It uses a powerful image model called VGG16 to extract features from images, unique characteristics that describe each image. 
PCA is used to choose the most important features, is useful for quickly analyzing images and finding the most important aspects.

- **Developed by:** S. Amoruso, M. Fusillo
- **Model type:** Convolutional Neural Network
- **Parent Model:** VGG16
- **Resources for more information:** https://www.tensorflow.org/api_docs/python/tf/keras/applications/VGG16



# Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

The model is intended to be used for image feature extraction and selection. 
Specifically, it serves as a tool to extract relevant features from images using the VGG16 convolutional neural network architecture. 
These features can then be utilized for various tasks such as image classification, object recognition, or other machine learning tasks that involve image data.

The foreseeable users of this model could be machine learning practitioners, data scientists, and researchers working in the field of computer vision. 
These individuals might use the code to quickly extract important features from images and reduce the dimensionality of the data using PCA

Those Affected by the Model:
The impact of the model extends to various stakeholders:

- **Developers/Researchers:** These individuals may benefit from a faster and automated way of processing and preparing image data for further analysis or model training.
- **End Users:** If the model contributes to improved accuracy and efficiency in downstream tasks like image classification, end users of applications that utilize these features might experience better performance.
- **Data Providers:** The model relies on the ImageNet dataset for pre-training. The data providers and curators of ImageNet could indirectly be affected by the model's use, as it demonstrates the value of their dataset in enabling diverse computer vision applications.


## Downstream Use

<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->

In the ecosystem projected the model will be used to extract information about logos inserted and in a second phase to make similarity between old logos and new logos
 



## Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->

The model's effectiveness is tied to image-related tasks. It won't be well-suited for tasks unrelated to image data, such as text analysis or time-series data.

The model's performance heavily relies on the quality and diversity of the ImageNet dataset. 
If the dataset doesn't cover the specific domain or features of interest, the extracted features might not be informative or relevant.

If the extracted features don't adequately capture the nuances of the target images, tasks requiring fine-grained details might suffer.




# Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

The model's performance heavily depends on the quality and diversity of the training 
data (ImageNet). If the data doesn't cover the variety of images in your application, 
the model might not capture the necessary features.

Extracted features might lack interpretability, making it challenging 
to understand why certain features are relevant for specific predictions

If the model is used to analyze personal images or data without consent, it could infringe on privacy rights. 
Care must be taken to handle sensitive data responsibly

## Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

To address bias, ensure your training data is diverse. 
Regularly evaluate predictions for bias and correct it using re-ranking or re-weighting techniques.

Manage risks by transparently communicating limitations to users. 
Conduct ethical reviews and secure sensitive data with access controls.

For technical improvements, fine-tune the model with your data, 
experiment with hyperparameters for optimal feature selection, 
and explore advanced architectures suited to your task.

Balancing these aspects will lead to responsible and effective model usage.



# Training Details

## Training Data

<!-- This should link to a Data Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

VGG16 was trained on the ImageNet dataset, 
specifically the ILSVRC dataset. The ILSVRC dataset contains around 1.2 million images for 
training and validation, categorized into 1,000 classes. 
This dataset is known for its diversity and size, making it suitable for training deep neural networks 
like VGG16.


## Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

### Preprocessing

1. Resizing: Images in the dataset are resized to a fixed resolution (usually 224x224 pixels)
2. Mean Subtraction: The mean pixel values of the entire dataset are subtracted from each image
3. Data Augmentation: Data augmentation techniques are often applied during training. 
These include random cropping, horizontal flipping, and sometimes color perturbations. 
These techniques increase the effective size of the training dataset and help the model become more robust.

### Speeds, Sizes, Times

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->

The training time for VGG16 can vary significantly based on hardware, software optimization, and dataset size. 
With powerful GPUs, it might take several days to train the model from scratch on the full ImageNet dataset.

It contains around 138 million parameters


 
# Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

## Testing Data, Factors & Metrics

### Testing Data

<!-- This should link to a Data Card if possible. -->


### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->

Several factors can influence the performance of VGG16 on the testing data: Data Quality, 
Data Distribution, Preprocessing, Noise and Variation

### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

Various metrics are used to quantify the performance of the VGG16 model on the testing data: 
- Top-1 Accuracy: This metric measures the percentage of images for which the correct class is the top prediction made by the model. It's a standard metric used in image classification tasks and is particularly relevant for models trained on the ImageNet dataset.
- Top-5 Accuracy: In addition to the top-1 accuracy, the top-5 accuracy measures the percentage of images for which the correct class is among the top 5 predictions.
- Precision and Recall
- F1-Score



# Model Examination

## Model Architecture and Objective

Feature Extraction: 
The VGG16 model is used for feature extraction the objective of this part is to 
transform input images into a set of high-level features that capture meaningful 
information about the content of the images.

Feature Selection: The objective here is to reduce the dimensionality of 
the extracted features using Principal Component Analysis (PCA). 
PCA identifies the most informative dimensions while minimizing loss of variance.

# Citation

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->

l Hassan, M., 2018. VGG16 – Convolutional Net-
work for Classification and Detection. Neurohive.
https://neurohive.io/en/popular-networks/vgg16/. 

Hewage, R., 2020. Extract features, visualize filters
and feature maps in vgg16 and vgg19 cnn models,
May. https://towardsdatascience.com/extract-
features-visualize-filters-and-feature-maps-in-
vgg16-and-vgg19-cnn-models-d2da6333edd0


# Model Card Authors

<!-- This section provides another layer of transparency and accountability. Whose views is this model card representing? How many voices were included in its construction? Etc. -->

S. Amoruso, M. Fusillo