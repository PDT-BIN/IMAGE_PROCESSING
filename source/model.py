import numpy as np
from PIL.Image import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array


class Model:
    def __init__(self):
        self.MODEL = load_model("model/model.h5")
        with open("model/label.txt", "r") as file:
            self.LABEL = file.read().split(", ")

    def predict(self, image: Image) -> str:
        # TRANSFORM IMAGE INTO NDARRAY.
        image = np.expand_dims(img_to_array(image.resize((224, 224))), [0])
        # PREDICT THE LABEL INDEX.
        index = self.MODEL.predict(image).argmax(axis=-1)[0]
        # RETURN ACTUAL LABEL.
        return self.LABEL[index]
