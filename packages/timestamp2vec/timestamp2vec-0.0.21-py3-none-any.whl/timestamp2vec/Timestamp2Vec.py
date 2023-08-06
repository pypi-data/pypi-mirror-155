from tensorflow.keras import Model
import keras
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer
import pathlib
import os

# from Timestamp2Vec_Class import helper_functions
from timestamp2vec.helper_functions import *

script_dir = os.path.dirname(__file__)
rel_path_encoder = "encoder_VAE"
abs_path_encoder = os.path.join(script_dir, rel_path_encoder)

class Timestamp2Vec(Model):
    def __init__(self):
        super(Timestamp2Vec, self).__init__()
        self.vectorize = Vectorize()
        self.encoder = keras.models.load_model(abs_path_encoder)
    
    def call(self, x):
        # vectorize the input into features
        x = self.vectorize(x)
        # obtain the latent variable and take the mean
        z = self.encoder.predict(x)[0]
        return z


class Vectorize(Layer):
    # Sampling layer of the VAE, creation of the latent variable z
    # The sampling layer uses as distribution a normal distribution
    def call(self, inputs):
        if type(inputs) == str:
            inputs = np.array([inputs])
        elif type(inputs) == list:
            inputs = np.array(inputs)
        inputs = np.array(list(map(np.datetime64, inputs)))
        inputs = inputs.astype('datetime64[ms]')
        inputs = np.array(list(map(extract_features_date, inputs)))
        inputs = np.array(list(map(normalize, inputs)))
        inputs = np.asarray(inputs).astype('float32')
        inputs = tf.reshape(inputs, [-1, 22])

        return inputs