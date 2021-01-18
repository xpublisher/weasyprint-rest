#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import logging

from flask import request, abort
from flask_restful import Resource
from werkzeug.utils import secure_filename

from ..util import authenticate
from ...print.weasyprinter import WeasyPrinter

class PrintAPI(Resource):
  decorators = [authenticate]

  def __init__(self):
    super(PrintAPI, self).__init__()

  def post(self):
    # check if the post request has the file part
    if 'html' not in request.files:
      return abort(422)

    html_files = request.files['html']
    css_files = request.files['css'] or []
    attachment_files = request.files['attachment'] or []
    font_files = request.files['font'] or []

    printer = WeasyPrinter()

    return {
      "status": "OK",
      "timestamp": round(time.time() * 1000)
    }, 200
