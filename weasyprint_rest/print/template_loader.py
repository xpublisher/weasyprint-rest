import json
import glob
import os
import logging
import mimetypes

from werkzeug.datastructures import FileStorage

from .template import Template
from ..env import is_debug_mode


class TemplateLoader:
    instance = None

    def __init__(self):
        if not TemplateLoader.instance:
            TemplateLoader.instance = TemplateLoader.__TemplateLoader()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __TemplateLoader:
        def __init__(self):
            self.template_definitions = {}

        def load(self, base_dir):
            for template_dir in os.listdir(base_dir):
                abs_template_dir = os.path.join(base_dir, template_dir)
                template_file = os.path.join(abs_template_dir, "template.json")
                if not os.path.isfile(template_file):
                    self.add_definition(abs_template_dir, {})
                    continue
                with open(template_file) as json_file:
                    self.add_definition(abs_template_dir, json.load(json_file))

        def add_definition(self, base_dir, definition):
            name = definition["name"] if "name" in definition else os.path.basename(base_dir)
            if name in self.template_definitions:
                logging.warn(
                    "Template %r found in %r was already defined. This template will be ignored" % (name, base_dir))
                return

            definition["name"] = name
            definition["base_dir"] = base_dir
            definition["prepared"] = False
            definition["template"] = None
            self.template_definitions[name] = definition

        def get(self, name):
            if name not in self.template_definitions:
                return None

            definition = self.template_definitions[name]

            if not definition["prepared"] or is_debug_mode():
                self._prepare_definition(definition)

            if not definition["template"] or is_debug_mode():
                self._build_template(definition)

            return definition["template"]

        def _prepare_definition(self, definition):
            base_dir = definition["base_dir"]

            if "styles" not in definition:
                definition["styles"] = self._detect_file_locations(base_dir, "**/*.css")

            if "assets" not in definition:
                definition["assets"] = self._detect_file_locations(base_dir, "**/*")

            definition["prepared"] = True

        def _detect_file_locations(self, base_dir, search_pattern):
            return [
                name for name in glob.glob(os.path.join(base_dir, search_pattern), recursive=True)
            ]

        def _build_template(self, definition):
            base_dir = definition["base_dir"]

            styles = self._read_files(base_dir, definition["styles"])
            assets = self._read_files(base_dir, definition["assets"])

            template = Template(styles=styles, assets=assets)
            definition["template"] = template

        def _read_files(self, base_dir, file_locations):
            files = []
            for file in file_locations:
                if not os.path.isfile(file):
                    continue

                files.append(FileStorage(
                    stream=open(file, "rb"),
                    filename=os.path.relpath(file, base_dir),
                    content_type=mimetypes.guess_type(file)[0]
                ))
            return files
