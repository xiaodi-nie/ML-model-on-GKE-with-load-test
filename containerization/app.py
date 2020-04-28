from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging

import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""

    LOG.info(f"Scaling Payload: {payload}")
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    html = f"<h3>Titanic Prediction Home</h3>"
    return html.format(format)

# TO DO:  Log out the prediction value
@app.route("/predict", methods=['POST'])
def predict():
    """Performs a prediction

    input looks like:
        {
          "Pclass": {
            "0": 1
          },
          "Sex": {
            "0": 1
          },
          "Age": {
            "0": 5
          },
          "SibSp": {
            "0": 1
          },
          "Parch": {
            "0": 0
          },
          "Fare": {
            "0": 3
          },
          "Embarked": {
            "0": 1
          },
          "relatives": {
            "0": 1
          },
          "not_alone": {
            "0": 0
          },
          "Deck": {
            "0": 3
          },
          "Title": {
            "0": 3
          }
        }
    result looks like:
    { "survive_or_not": [ 1 ] }

    """


    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"inference payload DataFrame: {inference_payload}")
    prediction = list(clf.predict(inference_payload))
    for idx, item in enumerate(prediction):
      if(item==1):
        prediction[idx]='Survived!'
      else:
        prediction[idx]='Sorry:('
    return jsonify({'survive_or_not': prediction})

if __name__ == "__main__":
    clf = joblib.load("Titanic_prediction_updated.joblib")
    app.run(host='0.0.0.0', port=8080, debug=True)
