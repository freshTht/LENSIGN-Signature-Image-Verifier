import json
from src import ls_models

import flask
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/model/classify', methods=['GET'])
def test():
  json = request.get_json()
  x = json['x']
  results = ls_models.predict(x)
  return flask.jsonify({
    'success': True,
    'data': {
      # 'input': x,
      'result': results
    },
  })

@app.route('/model/input-shape', methods=['GET'])
def input_shape():
  input_shape = ls_models.get_input_shape()
  return flask.jsonify({
    'success': True,
    'data': input_shape,
  })

# @app.route('/test-params', methods=['GET', 'POST'])
# def test_params():
#   json = request.get_json()
#   form_data = request.form    # body (form data)
#   params = request.args       # args (in url)
#   return flask.jsonify({
#     'success': True,
#     'data': {
#       'json': json,
#       'form_data': form_data,
#       'params': params,
#     }
#   })

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)