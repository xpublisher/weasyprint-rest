import os
import gc

from weasyprint import HTML

from .template import Template


class WeasyPrinter():

  def __init__(self, html, template=None):
    self.html = html
    self.template = template if template is not None else Template()

  def write(self, mode="pdf"):
    html = HTML(file_obj=self.html, encoding="utf-8", url_fetcher=self.template.url_fetcher, base_url=os.getcwd())
    font_config = self.template.get_font_config()
    styles = self.template.get_styles() if self.template is not None else []

    if mode == "pdf":
      result = html.write_pdf(stylesheets=styles, image_cache=None, font_config=font_config)
      # Sorry for the duplicate but im not sure this can be done in an extra method :/
      del html
      del font_config
      del styles
      gc.collect()
      return result

    if mode == "png":
      result = html.write_png(stylesheets=styles, image_cache=None, font_config=font_config)
      del html
      del font_config
      del styles
      gc.collect()
      return result
