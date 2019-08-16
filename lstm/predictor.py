# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

import os
import json
import pickle
import sys
import numpy as np
from flask import Flask, Response, request
from keras.optimizers import RMSprop
from keras.models import model_from_json

from dataset import TitleDataset

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.
class ScoringService(object):
    model = None                # Where we keep the model when it's loaded
    dataset = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model is None:
            with open(os.path.join(model_path, 'model_architecture.json'), 'r') as f:
                cls.model = model_from_json(f.read())

            cls.model.summary()
            optimizer = RMSprop(lr=0.01)
            cls.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

            cls.model.load_weights(os.path.join(model_path, 'model_weights.hdf5'))
        return cls.model

    @classmethod
    def get_dataset(cls):
        """Get the dataset object for this instance, loading it if it's not already loaded."""
        if cls.dataset is None:
            with open(os.path.join(model_path, 'model_dataset.pickle'), 'rb') as f:
                cls.dataset = pickle.load(f)
        return cls.dataset

    @classmethod
    def sample(cls, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.
        Args:
            input string: The data on which to do the predictions."""
        model = cls.get_model()
        dataset = cls.get_dataset()

        diversity = 0.2

        generated = ''
        sentence = input
        generated += sentence
        sentence = sentence[-dataset.max_len:]
        print(f'----- Generating with seed: "{sentence}"')
        for i in range(100):
            x_pred = np.zeros((1, dataset.max_len, len(dataset.chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, dataset.char2idx[char]] = 1.0

            preds = model.predict(x_pred, verbose=0)
            preds = preds[0]
            next_index = cls.sample(preds, diversity)
            next_char = dataset.idx2char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            if next_char == '\n':
                break
        return generated


# The flask app for serving predictions
app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None and ScoringService.get_model() is not None

    status = 200 if health else 404
    return Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    seed = request.form['title']

    if seed is None or seed == '' or 7 > len(seed) or len(seed) > 30:
        print(f'Invalid seed: {seed}')
        return Response(response='\n', status=200)

    # Do the prediction
    gen_title = ScoringService.predict(seed)

    return Response(response=gen_title, status=200)
