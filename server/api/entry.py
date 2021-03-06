
import numpy as np
from flask import json

import sys
sys.path.append("../classifiers")
from classifiers_predict import ClassifierHandler

from flask import Flask, url_for
from flask import request


app = Flask(__name__)


@app.route('/messages', methods = ['POST'])
def api_message():
  if request.headers['Content-Type'] == 'text/plain':
    return "Text Message: " + request.data
  elif request.headers['Content-Type'] == 'application/json':
    return "JSON Message: " + json.dumps(request.json)
  elif request.headers['Content-Type'] == 'audio/wav':
    # Convert binary string to numpy array of ints. Write to .wav fileformat
    signal = np.fromstring(request.data, dtype=np.int32)
    classify_type = request.headers['Classifier']
    classifyHandler = ClassifierHandler()
    if signal.shape[0] < classifyHandler.SIGNAL_LENGTH:
      response = {
        'message': "400 Error, to short audio length. Received " + str(round(signal.shape[0] / float(classifyHandler.HZ),2) )+ " second audio but needs 30 seconds to classify a genre."
      }
      return json.dumps(response)

    

    if classify_type == 'k_nearest':
      k = request.headers['K']
      classifyHandler.setK(k)
    genre_label, file_name = classifyHandler.selectClassifierAndPredict(classify_type, signal)
    response = {
      'message': "Processed .wav file succesfully. Audio file saved as " + file_name ,
      'genre': genre_label
    }
    return json.dumps(response)
  else:
    # request.data gives the same result as using FormData on client side
    # and using request.files['file']
    print request.data
    return "415 unsupported media type"

if __name__ == '__main__':
  app.run()
