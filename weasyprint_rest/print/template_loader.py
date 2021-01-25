import json, glob, os, logging, mimetypes

from werkzeug.datastructures import FileStorage

from .template import Template

class TemplateLoader:

  instance = None
  def __init__(self):
    if not TemplateLoader.instance:
      TemplateLoader.instance = TemplateLoader.__TemplateLoader()

  def __getattr__(self, name):
    return getattr(self.instance, name)

  class __TemplateLoader:
    def __init__(self):
      self.template_defintions = {}

    def load(self, base_dir): 
      for template_dir in os.listdir(base_dir):
        abs_template_dir = os.path.join(base_dir, template_dir);
        template_file = os.path.join(abs_template_dir, "template.json")
        if not os.path.isfile(template_file):
          self.add_definition(abs_template_dir, {})
          continue
        with open(template_file) as json_file:
          self.add_definition(abs_template_dir, json.load(json_file))

    def add_definition(self, base_dir, definition):
      name = definition["name"] if "name" in definition else os.path.basename(base_dir)
      if name in self.template_defintions:
        logging.warn("Template %r found in %r was already defined. This template will be ignored" % (name, base_dir))
        return

      definition["name"] = name
      definition["base_dir"] = base_dir
      definition["prepared"] = False
      definition["template"] = None
      self.template_defintions[name] = definition

    def get(self, name):
      if name not in self.template_defintions:
        return None

      definition = self.template_defintions[name]

      if not definition["prepared"]:
        self._prepare_definition(definition)

      # if not definition["template"]:
      self._build_template(definition)

      return definition["template"]

    def _prepare_definition(self, definition): 
      if "styles" not in definition:
        definition["styles"] = [name for name in glob.glob(os.path.join(definition["base_dir"], "**/*.css"), recursive = True)] 

      if "assets" not in definition:
        definition["assets"] = [name for name in glob.glob(os.path.join(definition["base_dir"], "**/*"), recursive = True)] 

      definition["prepared"] = True

    def _build_template(self, definition): 
      base_dir = definition["base_dir"]

      styles = []
      for style_file in definition["styles"]:
        styles.append(FileStorage(
          stream=open(style_file, "rb"),
          filename=os.path.relpath(style_file, base_dir),
          content_type=mimetypes.guess_type(style_file)[0]
        ))

      assets = []
      for asset_style in definition["assets"]:
        assets.append(FileStorage(
          stream=open(asset_style, "rb"),
          filename=os.path.relpath(asset_style, base_dir),
          content_type=mimetypes.guess_type(asset_style)[0]
        ))

      template = Template(styles = styles, assets = assets)
      definition["template"] = template
