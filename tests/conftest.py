import pytest
from weasyprint_rest.app import create_app

_app = None


@pytest.fixture
def app():
  global _app  # pylint: disable=global-statement
  if _app is None:
    _app = create_app()
  return _app
