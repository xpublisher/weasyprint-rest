import re
import os
import io
import logging
from weasyprint import HTML, CSS, Attachment, default_url_fetcher
from weasyprint.fonts import FontConfiguration

from ..web.util import check_url_access

UNICODE_SCHEME_RE = re.compile('^([a-zA-Z][a-zA-Z0-9.+-]+):')


class WeasyPrinter():
  def __init__(self, html, css = None, attachments = None, fonts = None):
    self.html = html

    if css != None:
      self.css = {item.filename: item for item in css}

    if attachments != None:
      self.attachments = {item.filename: item for item in attachments}

    if fonts != None:
      self.fonts = {item.filename: item for item in fonts}


  def write(self, mode="pdf"):
    html = HTML(file_obj=self.html, encoding="utf-8", url_fetcher=self._url_fetcher)
    font_config = FontConfiguration()

    if self.css == None:
      css = []
    else:
      css = [CSS(file_obj=sheet, url_fetcher=self._url_fetcher, font_config=font_config) for key, sheet in self.css.items()]

    return html.write_pdf(stylesheets=css, image_cache=None, font_config=font_config)

  def _url_fetcher(self, url):
    if not UNICODE_SCHEME_RE.match(url): # pragma: no cover
      raise ValueError('Not an absolute URI: %r' % url)

    if url.startswith('file://'):
      return self._resolve_file(url.split('?')[0])

    if not check_url_access(url):
      raise PermissionError('Requested URL %r was blocked because of restircion definitions.' % url)
    return default_url_fetcher(url)

  def _resolve_file(self, url):
    absFilePath = re.sub("^file://", "", url)
    filePath = os.path.relpath(absFilePath, os.getcwd()) 

    file = None
    # if filePath in self.css:
    #   # file = self.css[filePath]
    #   raise Exception('Ignore file %r was not found.')
    if filePath in self.attachments:
      file = self.attachments[filePath]
    
    if file == None:
      raise FileNotFoundError('File %r was not found.' % filePath)

    return  {
      'mime_type': file.mimetype,
      'file_obj': file,
      'filename': filePath
    }



