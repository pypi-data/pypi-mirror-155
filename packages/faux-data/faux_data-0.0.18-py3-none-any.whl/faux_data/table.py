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

import logging
import os
from dataclasses import dataclass, field
from typing import List

import numpy as np
import pandas as pd
import yaml

from .column import Column
from .factory import ColumnFactory, TargetFactory
from .target import Target
from .utils import load_csv_with_types, normalise_path, GCS_PREFIX

pd.set_option("max_colwidth", 180)

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Table:
    template_dir: str | None
    name: str
    rows: int
    columns: List[Column]
    targets: List[Target] = field(default_factory=list, repr=False)
    output_columns: List[str] = field(default_factory=list)
    df: pd.DataFrame = None
    complete: bool = False
    error: Exception = None

    @classmethod
    def parse_from_yaml(cls, yaml_str):
        conf = yaml.safe_load(yaml_str)
        return cls(**conf)

    def __init__(self,
                 name: str,
                 rows: int | str,
                 columns: list,
                 template_dir: str = None,
                 output_columns: list = None,
                 targets: list = None):
        try:
            self.template_dir = template_dir
            self.name = name
            self.rows = rows
            self.columns = self.parse_cols(columns)
            self.targets = self.parse_targets(targets)
            self.output_columns = output_columns if output_columns else None

        except Exception as e:
            self.complete = False
            log.error(e)
            raise TableParsingException(f"Error on table [{self.name}]. {e}")

    def parse_cols(self, columns) -> list:
        cols = []
        for column in columns:
            cols.append(ColumnFactory.parse(column))

        return cols

    def parse_targets(self, targets) -> list:
        targs = []

        if not targets:
            return targs

        for target in targets:
            try:
                targs.append(TargetFactory.parse(target))
            except Exception as e:
                log.warning(f"unable to parse target - {e}")
                pass

        return targs

    def create_df(self) -> pd.DataFrame:
        if isinstance(self.rows, int):
            return pd.DataFrame({"rowId": np.arange(self.rows)})
        else:

            if self.rows.startswith("/") or self.rows.startswith(GCS_PREFIX):
                # absolute path
                filepath = self.rows
            elif self.template_dir is None:
                raise Exception(
                    "rows: is a relative path but the template_dir was not available"
                )
            else:
                filepath = normalise_path(
                    os.path.join(self.template_dir, self.rows))

            log.debug(f"loading csv from {filepath}")
            return load_csv_with_types(filepath)

    def generate(self) -> None:
        """Generates the table data"""
        try:
            self.df = self.create_df()
            for column in self.columns:
                column.maybe_add_column(self.df)

        except Exception as e:
            self.complete = False
            self.error = TableGenerationException(
                f"Error on table [{self.name}]. {e}")

            raise self.error

        else:
            self.df.drop(columns="rowId", inplace=True)

            if self.output_columns:
                self.df = self.df[self.output_columns]

            self.complete = True

    def load(self):
        """Loads `self.df` to the specified targets"""
        if not self.targets:
            print("No targets!")

        try:
            for target in self.targets:
                target.save(self)

        except Exception as e:
            self.complete = False
            self.error = TableLoadingException(
                f"Error on table [{self.name}]. {e}")

            raise self.error

    def run(self):
        self.generate()
        self.load()

    def result(self):
        return "yope"


class TableParsingException(Exception):
    pass


class TableGenerationException(Exception):
    pass


class TableLoadingException(Exception):
    pass
