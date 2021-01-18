from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

def url_fetcher(url):
  pass

class WeasyPrinter():
  def __init__(self, html, css, attachments, fonts):
    self.html = html or ""
    self.css = css or []
    self.attachments = attachments or []
    self.fonts = fonts or []

  def write(self, mode):
    # TODO add url_fetcher to increase security
    html = HTML(string=self.html, encoding="utf-8")
    css = [CSS(string=sheet) for sheet in self.css]

    # mode = mode or "pdf"
    
    return html.write_pdf(stylesheets=css)
