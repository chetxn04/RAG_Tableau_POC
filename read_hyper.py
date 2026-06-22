from tableauhyperapi import HyperProcess, Connection, Telemetry, TableName
import pandas as pd

def hyper_to_dataframe(hyper_path):
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hp:
        with Connection(endpoint=hp.endpoint, database=hyper_path) as conn:
            schema_names = conn.catalog.get_schema_names()
            print(f"Schemas found: {schema_names}")

            all_dfs = {}
            for schema in schema_names:
                table_names = conn.catalog.get_table_names(schema=schema)
                if not table_names:
                    continue
                print(f"Tables in schema '{schema}': {table_names}")

                for table in table_names:
                    table_def = conn.catalog.get_table_definition(table)
                    columns = [c.name.unescaped for c in table_def.columns]
                    rows = conn.execute_list_query(f'SELECT * FROM {table}')
                    df = pd.DataFrame(rows, columns=columns)
                    key = table.name.unescaped
                    all_dfs[key] = df
                    print(f"  -> '{key}': {len(df)} rows, {len(columns)} columns")
            return all_dfs

print("=== SUPERSTORE ===")
superstore_tables = hyper_to_dataframe("extracted_superstore/Data/Extracts/Sample _ Superstore _copy_.hyper")

print("\n=== COVID ===")
covid_tables = hyper_to_dataframe("extracted_covid/Data/Outputs/COVID-19 Activity.hyper")