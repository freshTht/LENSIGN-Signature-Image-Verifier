import json
from .controllers import ls_models, ls_firebase
from . import ls_image_classifier

import flask
from flask import Flask, request

UPLOAD_FOLDER = './tmp/sigver-images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/model/classify', methods=['GET', 'POST'])
def test():
  json = request.get_json()
  x = json['x']
  n = len(x)

  # equal-width sampling
  REQUIRED_N = ls_models.get_input_shape()[0]
  step = (n-1) / (REQUIRED_N-1)
  decimal_i = 0

  indexes = []
  sampled_x = []
  while len(indexes) < REQUIRED_N:
    i = int(decimal_i)
    indexes.append(i)
    sampled_x.append(x[i])
    decimal_i += step

  # y = ls_models.predict(x)
  sampled_y = ls_models.predict(sampled_x)
  return flask.jsonify({
    'success': True,
    'data': {
      # 'raw': {
      #   'input-size': n,
      #   'result': y,
      # },
      'sampled': {
        'input-size': len(indexes),
        'result': sampled_y,
      }
    },
  })

@app.route('/model/input-shape', methods=['GET'])
def input_shape():
  input_shape = ls_models.get_input_shape()
  return flask.jsonify({
    'success': True,
    'data': input_shape,
  })

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

@app.route('/model/image/classify/<user_id>/', methods=['GET','POST'])
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

#
# Firebase
#
@app.route('/training/datasets', methods=['GET'])
def datasets_list():
  result = ls_firebase.datasets.list_all()

  return flask.jsonify({
    'success': True,
    'data': result
  })

@app.route('/training/datasets', methods=['POST'])
def datasets_new():
  json = request.get_json()
  form_data = request.form    # body (form data)

  if json != None:
    result = ls_firebase.datasets.add(json['name'])
  else:
    result = ls_firebase.datasets.add(form_data['name'])

  return flask.jsonify({
    'success': True,
    'data': result
  })

@app.route('/training/datasets/<id>/signatures', methods=['GET'])
def datasets_list_signatures(id):
  result = ls_firebase.datasets.list_signatures(id)
  return flask.jsonify({
    'success': True,
    'data': result
  })

@app.route('/training/datasets/<id>/signatures', methods=['POST'])
def datasets_new_signature(id):
  json = request.get_json()
  result = ls_firebase.datasets.add_signature(id, json['signature'])
  return flask.jsonify({
    'success': True,
    'data': result
  })

# WIP
# @app.route('/training/datasets/<id>/signatures/execute', methods=['POST'])
# def datasets_new_signature(id):
#   json = request.get_json()
#   result = ls_firebase.datasets.add_signature(id, json['signature'])
#   return flask.jsonify({
#     'success': True,
#     'data': result
#   })

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)