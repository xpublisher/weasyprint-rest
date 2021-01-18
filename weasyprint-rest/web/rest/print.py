#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import logging

from weasyprint import Attachment
from flask import request, abort, make_response
from flask_restful import Resource

from ..util import authenticate
from ...print.weasyprinter import WeasyPrinter

def parse_request_content():
  files = request.files

  html_files =  files["html"]
  css_files =  files.getlist("css") if "css" in files else []
  attachment_files = files.getlist("attachment") if "attachment" in files else []
  font_files = files.getlist("font") if "font" in files else []

  return html_files, css_files, attachment_files, font_files

class PrintAPI(Resource):
  decorators = [authenticate]

  def __init__(self):
    super(PrintAPI, self).__init__()

  def post(self):
    # check if the post request has the file part
    if 'html' not in request.files:
      return abort(422)

    # get arguments and convert to pdf
    html, css, attachments, fonts = parse_request_content()

    printer = WeasyPrinter(html, css, attachments, fonts)
    pdf = printer.write()

    # build response 
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    basename, _ = os.path.splitext(html.filename)
    response.headers['Content-Disposition'] = 'inline;filename=%s' % (basename + ".pdf")
    return response

