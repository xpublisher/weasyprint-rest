#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

import re
import logging

from flask import Flask, abort, request
from flask_restful import Api
from functools import wraps

from ..env import (get_api_key, get_allowed_url_pattern, get_blocked_url_pattern,
  get_max_upload_size, is_debug_mode, get_secret_key)

app = Flask(__name__, static_url_path="")

# set configurations
app.config['MAX_CONTENT_LENGTH'] = get_max_upload_size()
app.config['DEBUG'] = is_debug_mode()
app.config['MAIL_ENABLED'] = False
app.config['SECRET_KEY'] = get_secret_key()

api = Api(app)


def authenticate(func):
  @wraps(func)
  def verify_token(*args, **kwargs):
    try:
      authenticated = (get_api_key() is None or
      ('X_API_KEY' in request.headers and get_api_key() == request.headers['X_API_KEY']))
    except:  # noqa: E722
      return abort(401)

    if authenticated is True:
      return func(*args, **kwargs)
    else:
      abort(401)

  return verify_token

def check_url_access(url): 
  allowed_url_pattern = get_allowed_url_pattern()
  blocked_url_pattern = get_blocked_url_pattern()

  try:
    if re.match(allowed_url_pattern, url):
      return True
    if re.match(blocked_url_pattern, url):
      return False
    return True
  except:  # noqa: E722
    logging.error("Could not parse one of the URL Patterns correctly. Therefor the URL %r was " +
      "blocked. Please check your configuration." % url)
    return False
