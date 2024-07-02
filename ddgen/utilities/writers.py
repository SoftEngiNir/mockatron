from __future__ import annotations

import pandas as pd

from ddgen.dummy_generator.generator import DummyGenerator


def csv_dump(path: str, ddgen: DummyGenerator):
    for table in ddgen.database:
        table_data = {key: ddgen.data_dict[key] for key in table.columns}
        table_df = pd.DataFrame(table_data)
        table_df.to_csv(f'{path}/{table.name}.csv', index=False)
