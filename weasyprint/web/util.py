#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, abort, request
from flask_restful import Api
from functools import wraps

import os

app = Flask(__name__, static_url_path="")
api = Api(app)


# TODO security
# from werkzeug.utils import secure_filename
# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def authenticate(func):
  @wraps(func)
  def verify_token(*args, **kwargs):

    try:
      # if 'X_API_KEY' not in request.headers or os.environ.get('X_API_KEY') == request.headers['X_API_KEY']:
      if 'X_API_KEY' in request.headers and os.environ.get('X_API_KEY') == request.headers['X_API_KEY']:
        return func(*args, **kwargs)
      else:
        abort(401)
    except:
      abort(401)

  return verify_token
