import pandas as pd
import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
import os

os.makedirs("gx/expectations", exist_ok=True)
os.makedirs("gx/validations", exist_ok=True)
os.makedirs("gx/uncommitted/data_docs", exist_ok=True)

context = gx.get_context(mode="file")

pandas_data_src = context.sources.add_pandas(name="pandas_source")
sql_data_src = context.sources.add_sqlite(
    name="sqlite_source",
    connection_string="sqlite:///data/sales_warehouse.db"
)


reference_asset = pandas_data_src.add_csv_asset(
    name="reference_data",
    filepath_or_buffer="data/historical_sales.csv",
)
sql_asset = sql_data_src.add_table_asset(
    name="daily_sales",
    table_name="daily_sales",
)

batch_request = reference_asset.build_batch_request()

assistant_result = context.assistants.onboarding.run(
    batch_request=batch_request,
    estimation="exact"
)

auto_suite = assistant_result.get_expectation_suite("auto_profile_suite")
context.add_expectation_suite(expectation_suite=auto_suite)

csv_batch_request = reference_asset.build_batch_request()

checkpoint_config_auto = {
    "name": "auto_profile_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": csv_batch_request,
            "expectation_suite_name": "auto_profile_suite",
        }
    ],
}

context.add_checkpoint(**checkpoint_config_auto)

result_auto = context.run_checkpoint(checkpoint_name="auto_profile_checkpoint")
print(f"First Checkpoint result: {'SUCCESS' if result_auto['success'] else 'FAIL'}")

manual_suite = context.add_expectation_suite("manual_validation_suite")

manual_suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "amount"},
    )
)

manual_suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "amount", "min_value": 0, "strict_min": True},
    )
)

manual_suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_match_regex",
        kwargs={
            "column": "user_email",
            "regex": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        },
    )
)

df_hist = pd.read_csv("data/historical_sales.csv")
hist = df_hist["category"].value_counts(normalize=True).to_dict()

partition_object = {
    "values": list(hist.keys()),
    "weights": list(hist.values()),
}

manual_suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_kl_divergence_to_be_less_than",
        kwargs={
            "column": "category",
            "partition_object": partition_object,
            "threshold": 0.3,
        },
    )
)

context.update_expectation_suite(manual_suite)

sql_batch_request = sql_asset.build_batch_request()

checkpoint_config_manual = {
    "name": "sql_validation_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": sql_batch_request,
            "expectation_suite_name": "manual_validation_suite",
        }
    ],
}

context.add_checkpoint(**checkpoint_config_manual)

result_manual = context.run_checkpoint(checkpoint_name="sql_validation_checkpoint")
print(f"Second Checkpoint result: {'SUCCESS' if result_manual['success'] else 'FAIL'}")

context.build_data_docs()
print("done")
