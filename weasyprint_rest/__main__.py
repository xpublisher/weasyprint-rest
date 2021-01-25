#!/usr/bin/python
# -*- coding: utf-8 -*-

from .env import is_debug_mode
from .app import app

if __name__ == '__main__':
  app().run(host='0.0.0.0', debug=is_debug_mode())
