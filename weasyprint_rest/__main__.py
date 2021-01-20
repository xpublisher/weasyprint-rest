#!/usr/bin/python
# -*- coding: utf-8 -*-

from logging
from waitress import serve
from .env import is_debug_mode, is_production_environment
from .app import create_app

if __name__ == '__main__':
  app = create_app()
  app.run(host='0.0.0.0', debug=is_debug_mode())
