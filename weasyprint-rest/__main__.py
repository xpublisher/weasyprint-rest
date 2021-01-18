#!/usr/bin/python
# -*- coding: utf-8 -*-

from .web.util import app, api
from .web.routes import register_routes

if __name__ == '__main__':
    register_routes(api)
    app.run(host='0.0.0.0')
