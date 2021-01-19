from .web.util import app, api
from .web.routes import register_routes

def create_app():
  _app = app()
  _api = api()

  register_routes(_api)
  return _app
