
#  Copyright (c) 2022.  Eugene Popov.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from witness.core.abstract import AbstractExtractor
from datetime import datetime
import pandas as pd
import logging

log = logging.getLogger(__name__)


class PandasExtractor(AbstractExtractor):
    """
    Basic pandas extractor class.
    Provides a single 'unify' method for all child pandas extractors.
    """
    def __init__(self, uri):
        super().__init__(uri)

    output: pd.DataFrame

    def _set_extraction_timestamp(self):
        setattr(self, 'extraction_timestamp', datetime.now())

    def extract(self):
        self._set_extraction_timestamp()

    def unify(self):

        data = self.output.to_dict(orient='records')
        meta = {'extraction_timestamp': self.extraction_timestamp,
                'record_source': self.uri}

        setattr(self, 'output', {'meta': meta, 'data': data})

        return self


class PandasFeatherExtractor(PandasExtractor):

    def extract(self):
        df = pd.read_feather(self.uri)
        setattr(self, 'output', df)
        super().extract()

        return self


class PandasExcelExtractor(PandasExtractor):

    def __init__(self, uri, sheet_name=0, header=0, dtype=None):
        self.sheet_name: str or int or None = sheet_name
        self.header: int = header
        self.dtype: str or dict or None = dtype
        super().__init__(uri)

    def extract(self):
        df = pd.read_excel(self.uri,
                           sheet_name=self.sheet_name,
                           header=self.header,
                           dtype=self.dtype)
        setattr(self, 'output', df)
        super().extract()

        return self

