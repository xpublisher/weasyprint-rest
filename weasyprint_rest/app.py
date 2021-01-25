

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .web.routes import register_routes
from .print.template_loader import TemplateLoader
from .env import (
  get_max_upload_size, get_template_directory, is_debug_mode,
  get_secret_key, is_cors_enabled, get_cors_origins
)

_app = None
_api = None


def create_app():
  global _app, _api
  _app = Flask(__name__)

  if is_cors_enabled():
    CORS(_app, resources={r"/api/*": {"origins": get_cors_origins()}})

  # set configurations
  _app.config['MAX_CONTENT_LENGTH'] = get_max_upload_size()
  _app.config['DEBUG'] = is_debug_mode()
  _app.config['MAIL_ENABLED'] = False
  _app.config['SECRET_KEY'] = get_secret_key()

  _api = Api(_app)

  register_routes(_api)
  TemplateLoader().load(get_template_directory())


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
