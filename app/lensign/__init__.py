import json
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
  
  files = {}
  for key in request.files:
    files[key] = request.files[key].filename

  return flask.jsonify({
    'success': True,
    'data': {
      'json': json,
      'form_data': form_data,
      'params': params,
      'files': files,
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
def sigver_classify_test(user_id):
  user_id = 10
  
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

IMG_UPLOAD_PATH = 'tmp/analyse'
@app.route('/model/image/analyse/', methods=['GET','POST'])
def sigver_analyse():
  ORIGINAL_IMG_URLS = request.form.getlist('original_images[]')
  ORIGINAL_IMAGES = []
  
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
  
  if not file:
    return flask.jsonify({
      'success': False,
      'message': 'No file found'
    })
  
  # save file
  filename = secure_filename(file.filename)
  filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename) 
  file.save(filepath)

  # URL = 'https://firebasestorage.googleapis.com/v0/b/lensign-wanda.appspot.com/o/users%2F11%2Fsig%2F1607312157477.png?alt=media&token=59e98115-5a35-4339-95f9-e713bf2c106b'
  for URL in ORIGINAL_IMG_URLS:

    # preprocess file name
    splitted = URL.split('/')
    FILE_NAME = splitted[len(splitted) - 1]
    file_name_with_token = FILE_NAME.split('?')
    FILE_NAME = file_name_with_token[0]
    FILE_PATH = IMG_UPLOAD_PATH + '/' + FILE_NAME

    # check if the file already exists
    already_exists = os.path.isfile(FILE_PATH)

    if not already_exists:
      print('downloading file: {}'.format(FILE_NAME))

      # download with wget
      stream = os.popen('wget "{}" -O {}'.format(URL,FILE_PATH))
      output = stream.read()
    else:
      print('file already exists: {}'.format(FILE_NAME))

    # check that the file exists
    success = os.path.isfile(FILE_PATH)
    # FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], FILE_PATH)
    
    if not success:
      continue

    # add to array
    ORIGINAL_IMAGES.append(FILE_PATH)

  # analyse
  res = ls_image_classifier.analyse(ORIGINAL_IMAGES, filepath)

  return flask.jsonify({
    'success': True,
    # 'data': {
    #   'success': success,
    #   'original': ORIGINAL_IMG_URLS,
    #   'results': res,
    # },
    'data': res
  })


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)