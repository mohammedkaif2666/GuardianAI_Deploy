# ai_engine_cnn.py
import os
# Force Keras 2 legacy behavior for your old model
os.environ["TF_USE_LEGACY_KERAS"] = "1" 

import pickle
import numpy as np
import tf_keras as keras # Use the legacy-support library
from tf_keras.models import model_from_json
from tf_keras.preprocessing.sequence import pad_sequences

class CNNBullyingDetector:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.max_length = 100 
        self._load_assets()

    def _load_assets(self):
        try:
            with open('tokenizer.pkl', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            
            with open('CNNmodel.json', 'r') as json_file:
                loaded_model_json = json_file.read()
                
            # Loading using the legacy-compatible model_from_json
            self.model = model_from_json(loaded_model_json)
            self.model.load_weights("CNNmodel_weights.h5")
            print("✅ CNN Legacy Model loaded successfully using compatibility layer.")
        except Exception as e:
            print(f"❌ CNN Error: {e}")

    def predict_text(self, text):
        if not self.model or not self.tokenizer: return 0.0
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post')
        prediction = self.model.predict(padded)
        return float(prediction[0][0])