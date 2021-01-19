#!/usr/bin/python
# -*- coding: utf-8 -*-

from .env import is_debug_mode
from .app import create_app

if __name__ == '__main__':
  app = create_app()
  app.run(host='0.0.0.0', debug=is_debug_mode())
