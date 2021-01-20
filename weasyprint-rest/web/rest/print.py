#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import request, abort, make_response
from flask_restful import Resource

from ..util import authenticate
from ...print.weasyprinter import WeasyPrinter


def parse_request_content():
  form = request.form
  args = request.args
  files = request.files

  if "mode" in form:
    mode = form["mode"]
  elif "mode" in args:
    mode = args["mode"]
  else:
    mode = "pdf"

  html_files = files["html"]
  css_files = files.getlist("css") if "css" in files else []
  attachment_files = files.getlist("attachment") if "attachment" in files else []

  return mode, html_files, css_files, attachment_files


class PrintAPI(Resource):
  decorators = [authenticate]

  def __init__(self):
    super(PrintAPI, self).__init__()

  def post(self):
    # check if the post request has the file part
    if 'html' not in request.files:
      return abort(422)

    # get arguments and convert to pdf
    mode, html, css, attachments = parse_request_content()

    printer = WeasyPrinter(html, css, attachments)
    content = printer.write(mode)

    # build response
    response = make_response(content)
    if mode == "pdf":
      basename, _ = os.path.splitext(html.filename)
      response.headers['Content-Type'] = 'application/pdf'
      response.headers['Content-Disposition'] = 'inline;filename=%s' % (basename + ".pdf")
    else:
      response.headers['Content-Type'] = '	image/png'

    return response
