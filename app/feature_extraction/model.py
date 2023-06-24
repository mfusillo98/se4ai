import keras
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
from keras.utils.image_utils import img_to_array, load_img
import numpy as np
import app.utils.files as files


# Create a feature extraction model by considering only the last dense layer of VGG 16 Neural Network
def get_feature_extraction_model():
    vgg16_model = keras.applications.VGG16(weights='imagenet', include_top=True)
    fe_model = Model(inputs=vgg16_model.input, outputs=vgg16_model.get_layer("fc2").output)
    return fe_model


# Process a generic image file in order to be passed to the feature extraction model
def get_image_processed_data(image_path, model):
    img = load_img(image_path, target_size=model.input_shape[1:3])
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def extract_features_from_url(url):
    tmp_path = files.get_abs_path("/_tmp")
    img_path = files.safe_image_download(url, tmp_path)
    if not img_path:
        raise Exception("Image path does not exists")
    model = get_feature_extraction_model()
    image_data = get_image_processed_data(img_path, model)
    return model.predict(image_data)[0]
