import os
import psutil

from weasyprint import HTML

from .template import Template

totalMemory = 0

class WeasyPrinter:

    def __init__(self, html, template=None):
        self.html = html
        self.template = template if template is not None else Template()

    def write(self, mode="pdf"):
        html = HTML(file_obj=self.html, encoding="utf-8", url_fetcher=self.template.url_fetcher, base_url=os.getcwd())
        font_config = self.template.get_font_config()
        styles = self.template.get_styles() if self.template is not None else []
        if mode == "pdf":

            print("REQUEST\n======================", flush=True)
            process = psutil.Process(os.getpid())
            memoryBefore = process.memory_info().rss / 1048576
            print('Memory before Request           : ' + str(round(memoryBefore, 2)) + 'mb', flush=True) # in mb
            global totalMemory
            if totalMemory == 0:
                totalMemory = memoryBefore

            result = html.write_pdf(stylesheets=styles, image_cache=None, font_config=font_config)

            process = psutil.Process(os.getpid())
            memoryAfter = process.memory_info().rss / 1048576
            print('Memory after Request            : ' + str(round(memoryAfter, 2)) + 'mb', flush=True) # in mb
            print('Difference                      : ' + str(round(memoryAfter - memoryBefore, 2)) + 'mb', flush=True) # in mb
            print('Memoy groth since Program start : ' + str(round(memoryAfter - totalMemory, 2)) + 'mb', flush=True) # in mb


            return result

        if mode == "png":
            return html.write_png(stylesheets=styles, image_cache=None, font_config=font_config)

    def close(self):
        self.template.close()
        self.html.close()
