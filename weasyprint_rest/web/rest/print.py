#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import io

from werkzeug.datastructures import MultiDict, FileStorage, ImmutableMultiDict
from flask import request, abort, make_response
from flask_restful import Resource

from ..util import authenticate
from ...print.weasyprinter import WeasyPrinter
from ...print.template_loader import TemplateLoader
from ...print.template import Template


def _parse_request_argument(name, default=None, parse_type=None, content_type=None, file_name=None):
  form = request.form
  args = request.args
  files = request.files

  content = default
  if name in form:
    content = form.getlist(name) if name.endswith("[]") else form[name]
  elif name in args:
    content = args.getlist(name) if name.endswith("[]") else args[name]
  elif name in files:
    content = files.getlist(name) if name.endswith("[]") else files[name]

  if parse_type == "file" and isinstance(content, str):
    return FileStorage(stream = io.BytesIO(bytes(content, encoding='utf8')), filename=file_name, content_type=content_type)

  if content == default and name.endswith("[]"):
    content = _parse_request_argument(name[:-2], default, parse_type, content_type, file_name)
    if not isinstance(content, list):
      return [content]

  return content


def _build_template():
  styles = _parse_request_argument("style[]", [], "file", "text/css", "style.css")
  assets = _parse_request_argument("asset[]", [])
  template_name = _parse_request_argument("template", None)
  base_template = TemplateLoader().get(template_name)

  return Template(styles=styles, assets=assets, base_template=base_template)


class PrintAPI(Resource):
  decorators = [authenticate]

  def __init__(self):
    super(PrintAPI, self).__init__()

  def post(self):
    mode = _parse_request_argument("mode", "pdf")
    html = _parse_request_argument("html", None, "file", "text/html", "document.html")
    if html is None:
      return abort(422, description="Required argument 'html' is missing.")

    template = _build_template()

    printer = WeasyPrinter(html, template=template)
    content = printer.write(mode)

    # build response
    response = make_response(content)
    if mode == "pdf":
      basename, _ = os.path.splitext(html.filename)
      response.headers['Content-Type'] = 'application/pdf'
      response.headers['Content-Disposition'] = 'inline;filename=%s' % (basename + ".pdf")
    else:
      response.headers['Content-Type'] = 'image/png'

    return response
