import logging

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .web.routes import register_routes
from .print.template_loader import TemplateLoader
from .env import (
    get_max_upload_size, get_template_directory, is_debug_mode,
    get_secret_key, is_cors_enabled, get_cors_origins
)

_global = {
    "app": None,
    "api": None
}


def create_app():
    local_app = Flask(__name__)

    if is_cors_enabled():
        CORS(local_app, resources={r"/api/*": {"origins": get_cors_origins()}})

    # set configurations
    local_app.config['MAX_CONTENT_LENGTH'] = get_max_upload_size()
    local_app.config['DEBUG'] = is_debug_mode()
    local_app.config['MAIL_ENABLED'] = False
    local_app.config['SECRET_KEY'] = get_secret_key()

    local_api = Api(local_app)

    register_routes(local_api)
    TemplateLoader().load(get_template_directory())

    weasyprint_logger = logging.getLogger("weasyprint")
    if is_debug_mode():
        weasyprint_logger.setLevel(logging.DEBUG)

    _global["app"] = local_app
    _global["api"] = local_api


def app():
    if _global["app"] is None:  # pragma: no cover
        create_app()
    return _global["app"]


def api():
    if _global["api"] is None:  # pragma: no cover
        create_app()
    return _global["api"]
