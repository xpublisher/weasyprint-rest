#!/usr/bin/python
# -*- coding: utf-8 -*-

from .rest.health import HealthAPI
from .rest.print import PrintAPI

def register_routes(api):
  api.add_resource(HealthAPI, '/api/v1.0/health')
  api.add_resource(PrintAPI, '/api/v1.0/print')
