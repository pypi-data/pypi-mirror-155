
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
from datetime import datetime

from witness.core.abstract import AbstractExtractor


def is_select(q: str) -> bool:
    return True if 'select' in str.lower(q) else False


class DatabaseExtractor(AbstractExtractor):

    def __init__(self, uri):
        super().__init__(uri)

    def _set_extraction_timestamp(self):
        setattr(self, 'extraction_timestamp', datetime.now())

    def extract(self):
        self._set_extraction_timestamp()

    def unify(self):
        raise NotImplementedError


class ODBCExtractor(DatabaseExtractor):

    def __init__(self, uri: str, query: str):
        self.uri: str = uri
        self.query: str = query if isinstance(query, str) and is_select(query) else None
        super().__init__(uri)

    def _set_extraction_timestamp(self):
        from datetime import datetime
        setattr(self, 'extraction_timestamp', datetime.now())

    def extract(self):
        from pyodbc import connect

        connector = connect(self.uri)
        cursor = connector.cursor()
        rows = cursor.execute(self.query).fetchall()

        self.output = {'description': cursor.description, 'rows': rows}
        super().extract()

        return self

    def unify(self):

        description = self.output['description']
        rows = self.output['rows']
        col_names = [col[0] for col in description]
        dtypes = [col[1] for col in description]
        source_dtypes = {col_names[i]: dtype for i, dtype in enumerate(dtypes)}

        def build_record(names, row):
            record = {names[i]: value for i, value in enumerate(row)}
            return record

        data = [build_record(col_names, row) for row in rows]
        meta = {'extraction_timestamp': self.extraction_timestamp,
                'record_source': self.uri,
                'source_dtypes': source_dtypes}

        setattr(self, 'output', {'meta': meta, 'data': data})

        return self
