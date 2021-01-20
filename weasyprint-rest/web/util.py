#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

import re
import logging

from flask import Flask, abort, request
from flask_restful import Api
from functools import wraps

from ..env import (
  get_api_key, get_allowed_url_pattern, get_blocked_url_pattern,
  get_max_upload_size, is_debug_mode, get_secret_key
)

_app = None
_api = None


def create_app():
  global _app, _api
  _app = Flask(__name__)

  # set configurations
  _app.config['MAX_CONTENT_LENGTH'] = get_max_upload_size()
  _app.config['DEBUG'] = is_debug_mode()
  _app.config['MAIL_ENABLED'] = False
  _app.config['SECRET_KEY'] = get_secret_key()

  _api = Api(_app)


def app():
  global _app
  if _app is None:  # pragma: no cover
    create_app()
  return _app


def api():
  global _api
  if _api is None:  # pragma: no cover
    create_app()
  return _api


def authenticate(func):
  @wraps(func)
  def verify_token(*args, **kwargs):
    try:
      authenticated = (
        get_api_key() is None
        or ('X_API_KEY' in request.headers and get_api_key() == request.headers['X_API_KEY'])
      )
    except:  # noqa: E722 # pragma: no cover
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
  except:  # noqa: E722 # pragma: no cover
    logging.error(
      "Could not parse one of the URL Patterns correctly. Therefor the URL %r was " +
      "blocked. Please check your configuration." % url
    )
    return False
