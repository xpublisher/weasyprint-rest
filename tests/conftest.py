import logging
import pytest
import importlib
app_module = importlib.import_module(".app", package='weasyprint-rest')

_app = None


@pytest.fixture
def app():
  global _app
  if _app is None:
    _app = app_module.create_app()
  return _app
