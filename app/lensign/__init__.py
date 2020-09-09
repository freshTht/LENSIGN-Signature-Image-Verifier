import json
from .controllers import ls_models, ls_firebase

import flask
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/model/classify', methods=['GET', 'POST'])
def test():
  json = request.get_json()
  x = json['x']
  n = len(x)

  # equal-width sampling
  REQUIRED_N = 120     # TODO: don't hard code this
  step = (n-1) / (REQUIRED_N-1)
  decimal_i = 0

  indexes = []
  sampled_x = []
  while len(indexes) < REQUIRED_N:
    i = int(decimal_i)
    indexes.append(i)
    sampled_x.append(x[i])
    decimal_i += step

  y = ls_models.predict(x)
  sampled_y = ls_models.predict(sampled_x)
  return flask.jsonify({
    'success': True,
    'data': {
      'raw': {
        'input-size': n,
        'result': y,
      },
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
# Firebase
#
@app.route('/training/datasets', methods=['GET'])
def datasets_list():
  result = ls_firebase.datasets.get_all()

  return flask.jsonify({
    'success': True,
    'data': result
  })

@app.route('/training/datasets', methods=['POST'])
def datasets_new():
  form_data = request.form
  result = ls_firebase.datasets.new(form_data['name'])
  return flask.jsonify({
    'success': True,
    'data': result
  })

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)