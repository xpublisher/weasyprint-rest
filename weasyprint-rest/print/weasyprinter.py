import re
import os
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration

from ..web.util import check_url_access

UNICODE_SCHEME_RE = re.compile('^([a-zA-Z][a-zA-Z0-9.+-]+):')


class WeasyPrinter():

  def __init__(self, html, css=None, attachments=None):
    self.html = html

    if css is not None:
      self.css = {item.filename: item for item in css}

    if attachments is not None:
      self.attachments = {item.filename: item for item in attachments}

  def write(self, mode="pdf"):
    html = HTML(file_obj=self.html, encoding="utf-8", url_fetcher=self._url_fetcher)
    font_config = FontConfiguration()

    if self.css is None:
      css = []
    else:
      css = ([
        CSS(file_obj=sheet, url_fetcher=self._url_fetcher, font_config=font_config) for _, sheet in self.css.items()
      ])

    if mode == "pdf":
      return html.write_pdf(stylesheets=css, image_cache=None, font_config=font_config)

    if mode == "png":
      return html.write_png(stylesheets=css, image_cache=None, font_config=font_config)

  def _url_fetcher(self, url):
    if not UNICODE_SCHEME_RE.match(url):  # pragma: no cover
      raise ValueError('Not an absolute URI: %r' % url)

    if url.startswith('file://'):
      return self._resolve_file(url.split('?')[0])

    if not check_url_access(url):
      raise PermissionError('Requested URL %r was blocked because of restircion definitions.' % url)
    return default_url_fetcher(url)

  def _resolve_file(self, url):
    abs_file_path = re.sub("^file://", "", url)
    file_path = os.path.relpath(abs_file_path, os.getcwd())

    file = None
    if file_path in self.attachments:
      file = self.attachments[file_path]

    if file is None:  # pragma: no cover
      raise FileNotFoundError('File %r was not found.' % file_path)

    return {
      'mime_type': file.mimetype,
      'file_obj': file,
      'filename': file_path
    }
