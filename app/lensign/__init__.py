import json
from .controllers import ls_firebase
from . import ls_image_classifier

import flask
from flask import Flask, request

UPLOAD_FOLDER = './tmp/sigver-images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

from werkzeug.utils import secure_filename
import os, signal

@app.route('/snap-snap', methods=['POST'])
def kill_server():
  os.kill(os.getpid(), signal.SIGINT)
  return flask.jsonify({ 
    "success": True, 
    "message": "Server is shutting down..." 
  })

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/test-params', methods=['GET', 'POST'])
def test_params():
  json = request.get_json()
  form_data = request.form    # body (form data)
  params = request.args       # args (in url)
  return flask.jsonify({
    'success': True,
    'data': {
      'json': json,
      'form_data': form_data,
      'params': params,
    }
  })

#
# SigVer (Image)
#
@app.route('/model/image/classify/test', methods=['GET'])
def sigver_test():
  res = ls_image_classifier.test()

  return flask.jsonify({
    'success': True,
    'data': res
  })

@app.route('/model/image/classify/<user_id>', methods=['GET','POST'])
def sigver_classify(user_id):
  user_ud = 10
  
  if 'file' not in request.files:
    return flask.jsonify({
      'success': False,
      'message': 'No file part'
    })

  file = request.files['file']
  if file.filename == '':
    return flask.jsonify({
      'success': False,
      'message': 'No file selected for uploading'
    })
    return redirect(request.url)
  
  if file:
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename) 

    file.save(filepath)
    # getPrediction(filename)
    # label, acc = getPrediction(filename)

    res = ls_image_classifier.get_distance(user_id, filepath)

    return flask.jsonify({
      'success': True,
      'data': res,
    })

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)