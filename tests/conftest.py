import pytest
from weasyprint_rest.app import app as application


@pytest.fixture
def app():
  return application()
