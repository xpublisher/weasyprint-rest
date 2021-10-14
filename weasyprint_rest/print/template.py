import re
import os
import mimetypes

from weasyprint import CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration

from .non_closable import NonClosable
from ..web.util import check_url_access

UNICODE_SCHEME_RE = re.compile('^([a-zA-Z][a-zA-Z0-9.+-]+):')
BASE64_DATA_RE = re.compile('^data:[^;]+;base64,')


class Template:
    def __init__(self, styles=None, assets=None, base_template=None):
        self.base_template = base_template
        self.font_config = FontConfiguration()

        if assets is not None:
            self.assets = {item.filename: item for item in assets}
        else:
            self.assets = {}

        if styles is not None:
            self.styles = ([
                CSS(
                    file_obj=sheet,
                    url_fetcher=self.url_fetcher,
                    font_config=self.font_config,
                    base_url=os.path.join(os.getcwd(), os.path.basename(sheet.filename))
                ) for sheet in styles
            ])
        else:
            self.styles = []

    def has_asset(self, name):
        if name in self.assets:
            return True
        return self.base_template.has_asset(name) if self.base_template is not None else False

    def get_asset(self, name):
        if name in self.assets:
            return self.assets[name]
        return self.base_template.get_asset(name) if self.base_template is not None else None

    def get_styles(self):
        return self.styles + (self.base_template.get_styles() if self.base_template is not None else [])

    def get_font_config(self):
        return self.font_config

    def url_fetcher(self, url):
        if not UNICODE_SCHEME_RE.match(url):  # pragma: no cover
            raise ValueError('Not an absolute URI: %r' % url)

        if url.startswith('file://'):
            return self._resolve_file(url.split('?')[0])

        if not check_url_access(url) and not BASE64_DATA_RE.match(url):
            raise PermissionError('Requested URL %r was blocked because of restircion definitions.' % url)

        fetch_result = default_url_fetcher(url)
        if fetch_result["mime_type"] == "text/plain":
            fetch_result["mime_type"] = mimetypes.guess_type(url)[0]

        return fetch_result

    def _resolve_file(self, url):
        abs_file_path = re.sub("^file://", "", url)
        file_path = os.path.relpath(abs_file_path, os.getcwd())

        file = None
        if self.has_asset(file_path):
            file = self.get_asset(file_path)

        if file is None:  # pragma: no cover
            raise FileNotFoundError('File %r was not found.' % file_path)

        mimetype = file.mimetype
        if mimetype in ["application/octet-stream", "text/plain"]:
            mimetype = mimetypes.guess_type(file_path)[0]

        return {
            'mime_type': mimetype,
            'file_obj': NonClosable(file),
            'filename': file_path
        }

    def __str__(self):
        return "Template {styles=" + str(self.styles) + ", assets=" + str(self.assets) + "}"
