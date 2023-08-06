#    Copyright 2022 @jack-tee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from __future__ import annotations

import base64
import logging
import os
from dataclasses import dataclass, field
from typing import List, Tuple

import yaml

from .config import settings
from .table import Table
from .template_rendering import render_template
from .utils import split_gcs_path, GCS_PREFIX

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Template:
    template_path: str | None = None
    variables: dict = field(default_factory=dict, repr=False)
    tables: List[Table]
    params: dict = field(default_factory=dict, init=False, repr=False)

    def __init__(self,
                 tables: dict,
                 template_path: str = None,
                 variables: dict = None):
        self.template_path = template_path
        self.variables = variables
        self.tables = [
            Table(template_dir=self.dirname, **table) for table in tables
        ]

    @property
    def dirname(self):
        return os.path.dirname(
            self.template_path) if self.template_path else None

    def generate(self):
        for table in self.tables:
            table.generate()

    def run(self):
        for table in self.tables:
            table.run()

    def result(self):
        return '/n'.join(t.result() for t in self.tables)

    @classmethod
    def from_string(cls,
                    template_str: str,
                    template_path: str = None,
                    params: dict[str, str] = {}) -> Template:
        """Instantiate a `Template` from a string."""

        rendered_template, _ = cls.render_template(template_str, params)
        parsed = yaml.safe_load(rendered_template)
        return cls(template_path=template_path, **parsed)

    @classmethod
    def from_base64_string(cls, base64_str: str) -> Template:
        """Instantiate a `Template` from a base64 encoded string."""

        template_str = base64.b64decode(base64_str).decode('utf-8')
        return cls.from_string(template_str)

    @classmethod
    def from_file(cls, filepath, params={}):
        log.info(
            f"instantiating Template from file: [{filepath}] with params: [{params}]"
        )

        if settings.deployment_mode == 'cloud_function' \
            or filepath.startswith(GCS_PREFIX):

            from google.cloud import storage
            client = storage.Client()

            if filepath.startswith(GCS_PREFIX):
                template_path = filepath
            else:
                template_path = f"{GCS_PREFIX}{settings.template_bucket}/{settings.template_location}/{filepath}"

            log.debug(
                f"retrieving file from cloud storage from path: [{template_path}]"
            )

            path = split_gcs_path(template_path)
            bucket = client.get_bucket(path.group("bucket"))

            template_str = bucket.get_blob(
                path.group("obj")).download_as_text()

        else:
            template_path = os.path.abspath(filepath)
            log.debug(f"loading file from filesystem [{template_path}]")
            with open(template_path, "r") as f:
                template_str = f.read()

        return cls.from_string(template_str, template_path, params)

    @classmethod
    def render_template(cls,
                        template_str,
                        params={}) -> Tuple[str, dict[str:str]]:
        """Renders a template string using the provided `params`."""
        log.debug(
            f"rendering template\n{template_str}\nwith params [{params}]")
        return render_template(template_str, params)

    @classmethod
    def render_from_file(cls, filepath, params) -> Tuple[str, dict[str:str]]:
        with open(filepath, "r") as f:
            template_str = f.read()
        return cls.render_template(template_str, params)
