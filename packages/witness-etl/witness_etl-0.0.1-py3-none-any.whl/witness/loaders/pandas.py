
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

from witness.core.abstract import AbstractLoader
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PandasLoader(AbstractLoader):

    def __init__(self, uri):
        super().__init__(uri)

    def prepare(self, batch):
        df = pd.DataFrame(batch.data, dtype='str')
        self.output = df
        return self

    def load(self):
        pass


class PandasSQLLoader(PandasLoader):
    """
    Loader that uses Pandas DataFrame.to_sql method for loading data.

    :param engine: sqlalchemy engine;
    :param table: name of the destination table;
    :param schema: name of the destination schema, None if not defined.
    """
    def __init__(self, engine, table: str, schema: str or None = None, **kwargs):

        self.engine = engine
        self.schema = schema
        self.table = table
        uri = f'{schema}.{table}'
        super().__init__(uri)

    def load(self):
        self.output.to_sql(name=self.table,
                           con=self.engine,
                           schema=self.schema,
                           if_exists='append',
                           method='multi')
        return self


class PandasExcelLoader(PandasLoader):

    def __init__(self, uri, sheet_name='Sheet1', **kwargs):
        self.sheet_name = sheet_name
        super().__init__(uri)

    def load(self):
        self.output.to_excel(
            excel_writer=self.uri,
            sheet_name=self.sheet_name
        )
        return self


class PandasFeatherLoader(PandasLoader):

    def __init__(self, uri):
        super().__init__(uri)

    def load(self):
        self.output.to_feather(self.uri)
        return self
