#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import io
import gc

from werkzeug.datastructures import FileStorage
from flask import request, abort, make_response
from flask_restful import Resource

from ..util import authenticate
from ...print.weasyprinter import WeasyPrinter
from ...print.template_loader import TemplateLoader
from ...print.template import Template


def _get_request_list_or_value(request_dict, name):
  return request_dict.getlist(name) if name.endswith("[]") else request_dict[name]


def _get_request_argument(name, default=None):
  form = request.form
  args = request.args
  files = request.files

  if name in form:
    return _get_request_list_or_value(form, name)
  elif name in args:
    return _get_request_list_or_value(args, name)
  elif name in files:
    return _get_request_list_or_value(files, name)
  return default


def _parse_request_argument(name, default=None, parse_type=None, parse_args=None):
  content = _get_request_argument(name, default)

  if parse_type == "file" and isinstance(content, str):
    content_type = _may_get_dict_value(parse_args, "content_type")
    file_name = _may_get_dict_value(parse_args, "file_name")
    return FileStorage(
      stream=io.BytesIO(bytes(content, encoding='utf8')),
      filename=file_name,
      content_type=content_type
    )

  if content == default and name.endswith("[]"):
    content = _parse_request_argument(name[:-2], default, parse_type, parse_args)
    if not isinstance(content, list):
      return [content]

  return content


def _may_get_dict_value(dict_values, key, default=None):
  if dict_values is None:
    return default
  if key not in dict_values:
    return default
  return dict_values[key]


def _build_template():
  styles = _parse_request_argument("style[]", [], "file", {
    "content_type": "text/css",
    "file_name": "style.css"
  })
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
    disposition = _parse_request_argument("disposition", "inline")
    html = _parse_request_argument("html", None, "file", {
      "content_type": "text/html",
      "file_name": "document.html"
    })

    if html is None:
      return abort(422, description="Required argument 'html' is missing.")

    template = _build_template()

    printer = WeasyPrinter(html, template=template)
    content = printer.write(mode)

    # build response
    response = make_response(content)
    basename, _ = os.path.splitext(html.filename)
    extension = None
    if mode == "pdf":
      response.headers['Content-Type'] = 'application/pdf'
      extension = "pdf"
    else:
      response.headers['Content-Type'] = 'image/png'
      extension = "png"

    response.headers['Content-Disposition'] = '%s; name="%s"; filename="%s.%s"' % (
      disposition,
      basename,
      basename,
      extension
    )

    del disposition
    del basename
    del extension
    del content
    del printer
    del template
    del mode
    del html
    gc.collect()

    return response
