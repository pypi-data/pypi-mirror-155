import datetime
import json
import os
import re
from collections.abc import Iterable, Callable
from functools import partial
from typing import List

from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType

from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3
from data_product_sdk.cortex_databricks.data_platform.databricks_utils import reset_autoloader_checkpoint
from data_product_sdk.cortex_databricks.data_platform.processing_utils import process_dataframe
from data_product_sdk.cortex_databricks.data_platform.profilling_utils import calculate_profilling
from data_product_sdk.cortex_databricks.data_platform.schema_utils import get_schema_from_s3
from data_product_sdk.cortex_databricks.data_platform.spark_utils import get_spark_session, ENVIRONMENT, check_table_exists, get_table_partitions, drop_table_duplicates, build_matching_sort_condition

LANDING_BUCKET = f'cortex-data-platform-landing-area-{ENVIRONMENT}'
BRONZE_BUCKET = f'cortex-databricks-bronze-{ENVIRONMENT}'
SILVER_BUCKET = f'cortex-databricks-silver-{ENVIRONMENT}'
GOLD_BUCKET = f'cortex-databricks-gold-{ENVIRONMENT}'

BRONZE_DB_NAME = f'cortex_databricks_bronze_{ENVIRONMENT}'
SILVER_DB_NAME = f'cortex_databricks_silver_{ENVIRONMENT}'
GOLD_DB_NAME = f'cortex_databricks_gold_{ENVIRONMENT}'


def __get_partition_type(partition_value: str):
    try:
        datetime.datetime.strptime(partition_value, '%Y-%m-%d')
        return 'date'
    except ValueError:
        return 'string'


def __resolve_partition_columns(path: str):
    pattern = r'(\w+)=(.*?)\/'
    partitions = re.findall(pattern, path)
    partitions = {i[0]: __get_partition_type(i[1]) for i in partitions}

    return partitions


def __list_partition_columns(s3_path: str):
    s3_bucket, s3_key = S3.get_bucket_key_from_s3_url(s3_url=s3_path)
    s3_client = S3(bucket_name=s3_bucket)
    s3_files = s3_client.list_s3_files(prefix=s3_key)  # TODO: TRAZER APENAS AS PASTAS
    if not s3_files:
        raise FileNotFoundError(f'No files found in the provided path: "{s3_path}"')
    s3_files = (__resolve_partition_columns(i['Key']) for i in s3_files)

    partitions = dict()
    for i in s3_files:
        for k, v in i.items():
            if partitions.get(k, v) != v:
                v = 'string'
            partitions.update({k: v})

    return partitions


def __build_schema_hints(js_schema: dict):
    if js_schema is None:
        return None
    fields = {i['name']: i['type'] for i in js_schema['fields'] if isinstance(i['type'], str)}
    schema_hints = ', '.join((f'{name} {type}' for name, type in fields.items()))

    return schema_hints


def __rename_invalid_columns(df: DataFrame) -> DataFrame:
    invalid_characters = "[ ,;{}()\n\t=\\/']"
    for col in df.columns:
        replace_col = re.sub(invalid_characters, '_', col)
        if col != replace_col:
            print(f'INVALID COLUMN NAME: {col} RENAMED AUTOMATICALLY TO -> {replace_col}')
        df = df.withColumnRenamed(col, replace_col)

    return df


def build_checkpoint_path(bucket_name: str, data_pack_name: str, dataset_name: str, input_table_name: str = ''):
    assert bucket_name == BRONZE_BUCKET or (input_table_name and bucket_name in (SILVER_BUCKET, GOLD_BUCKET)), \
        f'bucket name must be one of {BRONZE_BUCKET}, {SILVER_BUCKET} or {GOLD_BUCKET} and {input_table_name} must be valid when using {SILVER_BUCKET} or {GOLD_BUCKET}'
    checkpoint_location = f's3://{bucket_name}/_databricks_autoloader_checkpoints/{data_pack_name}/{dataset_name}/{input_table_name}'

    return checkpoint_location


def read_table(spark_session: SparkSession, db_name: str, table_name: str):
    table_name = f'{db_name}.{table_name}'
    df = spark_session.readStream.format('delta').table(tableName=table_name)

    return df


def read_data(spark_session: SparkSession, data_input_path: str, js_schema: dict, data_type: str, read_options: dict = None, infer_schema=False, data_pack_name=None,
              dataset_name=None):
    assert js_schema or infer_schema, f'js_schema not provided while infer_schema is {infer_schema}. Please provide a schema or turn schema inference on'
    if read_options is None:
        read_options = dict()

    df = spark_session.readStream. \
        format('cloudFiles'). \
        option('cloudFiles.format', data_type). \
        options(**read_options)
    if infer_schema:
        schema_hints = __build_schema_hints(js_schema=js_schema)
        schema_location = os.path.dirname(data_input_path)
        schema_location = os.path.join(schema_location, '_databricks_autoloader_schema')
        schema_location = os.path.join(schema_location, data_pack_name)
        schema_location = os.path.join(schema_location, dataset_name)
        schema_options = {'cloudFiles.schemaLocation': schema_location, 'cloudFiles.schemaHints': schema_hints}
        df = df.options(**schema_options)
    else:
        partitions = __list_partition_columns(data_input_path)
        for partition, partition_type in partitions.items():
            partition = {'metadata': dict(), 'name': partition, 'nullable': True, 'type': partition_type}
            js_schema['fields'].append(partition)
        schema = StructType.fromJson(js_schema)
        df = df.schema(schema)

    df = df.load(path=data_input_path)

    return df


def read_data_schema(spark_session: SparkSession, data_input_path: str, data_type: str, schema, read_options: dict = None):
    if read_options is None:
        read_options = dict()

    df = spark_session.readStream. \
        format('cloudFiles'). \
        option('cloudFiles.format', data_type). \
        options(**read_options)

    df = df.schema(schema)
    df = df.load(path=data_input_path)

    return df


def __upsert_function(micro_batch_df: DataFrame, batch_id: int, db_name, table_name, sort_fields: list, upsert_fields: list = None, spark=None):
    if spark is None:
        spark = get_spark_session('upsert_data')
    match_condition = build_matching_sort_condition(sort_fields=sort_fields, existing_df_name='current_df', inserting_df_name='micro_batch_df')

    micro_batch_df = micro_batch_df.sort(*sort_fields, ascending=False).drop_duplicates(subset=upsert_fields)
    current_df_name = 'current_df'
    micro_batch_df_name = 'micro_batch_df'
    upsert_condition = ' AND '.join([f'{current_df_name}.{i} = {micro_batch_df_name}.{i}' for i in upsert_fields])
    table_name = f'{db_name}.{table_name}'
    current_df = DeltaTable.forName(spark, table_name)
    current_df.alias(current_df_name).merge(micro_batch_df.alias(micro_batch_df_name), upsert_condition). \
        whenMatchedUpdateAll(match_condition). \
        whenNotMatchedInsertAll(). \
        execute()


# TODO: ADICIONAR PARAMETRO DE PATH
def write_table(df: DataFrame, checkpoint_location: str, db_name: str, table_name: str, spark=None, partition_columns=None, write_options: dict = None,
                sort_fields: list = None, upsert_fields: list = None):
    if partition_columns is None:
        partition_columns = list()
    if sort_fields is None:
        sort_fields = list()
    if write_options is None:
        write_options = dict()
    if spark is None:
        spark = get_spark_session('upsert_data')

    stream = df.writeStream.trigger(once=True) \
        .format('delta') \
        .option('checkpointLocation', checkpoint_location) \
        .options(**write_options)

    # TODO: MODULARIZAR
    if sort_fields and upsert_fields:
        if check_table_exists(spark=spark, db_name=db_name, table_name=table_name):
            print(f'TABELA EXISTE - upsert_fields: {upsert_fields} - sort_fields: {sort_fields}')
            upsert_func = partial(__upsert_function, db_name=db_name, table_name=table_name, sort_fields=sort_fields, upsert_fields=upsert_fields, spark=spark)
            stream = stream.foreachBatch(upsert_func)
            return stream.start()
        else:
            stream = stream.toTable(tableName=f'{db_name}.{table_name}', partitionBy=partition_columns)
            stream.awaitTermination()
            drop_table_duplicates(db_name=db_name, table_name=table_name, unique_id_fields=upsert_fields, sort_fields=sort_fields, spark=spark)
            return stream

    return stream.toTable(tableName=f'{db_name}.{table_name}', partitionBy=partition_columns)


def __apply_profiling(df: DataFrame, profiling_s3_bucket, profiling_s3_key):
    # check if dataframe is empty
    if df.count() == 0:
        raise ValueError('Dataframe is empty, profile aborted')
    else:
        profile_js = calculate_profilling(df)
        profile_js = json.dumps(profile_js)
        s3_client = S3(bucket_name=profiling_s3_bucket)

        return s3_client.put_object(profile_js, s3_key=profiling_s3_key)


def __apply_processing_function(df: DataFrame, func: Callable, args: list, kwargs: dict):
    if args is None:
        args = list()
    if kwargs is None:
        kwargs = dict()
    return func(df, *args, **kwargs)


def __apply_processing_functions(df: DataFrame, funcs: List[Callable], funcs_args: List[List], funcs_kwargs: List[dict]):
    assert len(funcs) == len(funcs_args) == len(funcs_kwargs), 'The size of all the parameters (functions, args and kwargs) must be equal'
    for func, args, kwargs in zip(funcs, funcs_args, funcs_kwargs):
        df = __apply_processing_function(df=df, func=func, args=args, kwargs=kwargs)
    return df


def apply_processing_function(df: DataFrame, func, func_args, func_kwargs):
    if func is None:
        return df
    if isinstance(func, Iterable):
        return __apply_processing_functions(df=df, funcs=func, funcs_args=func_args, funcs_kwargs=func_kwargs)
    else:
        return __apply_processing_function(df=df, func=func, args=func_args, kwargs=func_kwargs)


def apply_profiling(df: DataFrame, data_pack_name: str, dataset_name: str):
    # TODO: PARTICIONAR POR DATA
    profiling_s3_key = f'_databricks_profiling/{data_pack_name}/{dataset_name}.json'
    print(f'START PROFILING: {profiling_s3_key}')
    df.printSchema()
    df.show(5)
    __apply_profiling(df=df, profiling_s3_bucket=BRONZE_BUCKET, profiling_s3_key=profiling_s3_key)


def landing_to_bronze(data_input_path, data_type: str, data_pack_name, dataset_name, schema_path=None, partition_columns=None, spark=None,
                      read_options: dict = None, write_options: dict = None, profiling=False, infer_schema=False, reset_checkpoint=False):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()

    js_schema = get_schema_from_s3(schema_path)
    df = read_data(spark, data_input_path=data_input_path, js_schema=js_schema, data_type=data_type, read_options=read_options, infer_schema=infer_schema,
                   data_pack_name=data_pack_name, dataset_name=dataset_name)
    df = process_dataframe(df, js_schema=js_schema)
    df = __rename_invalid_columns(df)

    checkpoint_location = build_checkpoint_path(bucket_name=BRONZE_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name)
    stream = write_table(df, checkpoint_location=checkpoint_location, db_name=BRONZE_DB_NAME, table_name=dataset_name, spark=spark,
                         partition_columns=partition_columns, write_options=write_options)
    if reset_checkpoint:
        stream.awaitTermination()
        reset_autoloader_checkpoint(bucket_name=BRONZE_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(f'{BRONZE_DB_NAME}.{dataset_name}')
        apply_profiling(df=df, data_pack_name=data_pack_name, dataset_name=dataset_name)


def landing_to_bronze_schema(data_input_path, data_type: str, data_pack_name, dataset_name, schema=None, partition_columns=None, spark=None,
                             read_options: dict = None, write_options: dict = None, profiling=False, infer_schema=False):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()

    df = read_data_schema(spark, data_input_path=data_input_path, data_type=data_type, schema=schema,
                          read_options=read_options)

    # df = process_dataframe(df, js_schema=schema)
    df = __rename_invalid_columns(df)

    checkpoint_location = build_checkpoint_path(bucket_name=BRONZE_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name)
    stream = write_table(df, checkpoint_location=checkpoint_location, db_name=BRONZE_DB_NAME, table_name=dataset_name, spark=spark,
                         partition_columns=partition_columns, write_options=write_options)


def bronze_to_silver(input_table_name, data_pack_name, dataset_name, input_db_name=BRONZE_DB_NAME, partition_columns=None, spark=None,
                     write_options: dict = None, processing_function=None, processing_function_args=None, processing_function_kwargs=None, profiling=False,
                     reset_checkpoint=False):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()

    df = read_table(spark, db_name=input_db_name, table_name=input_table_name)
    df = apply_processing_function(df=df, func=processing_function, func_args=processing_function_args, func_kwargs=processing_function_kwargs)

    checkpoint_location = build_checkpoint_path(bucket_name=SILVER_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table_name)
    stream = write_table(df, checkpoint_location=checkpoint_location, db_name=SILVER_DB_NAME, table_name=dataset_name, spark=spark,
                         partition_columns=partition_columns, write_options=write_options)
    if reset_checkpoint:
        stream.awaitTermination()
        reset_autoloader_checkpoint(bucket_name=SILVER_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table_name)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(f'{SILVER_DB_NAME}.{dataset_name}')
        apply_profiling(df=df, data_pack_name=data_pack_name, dataset_name=dataset_name)


def silver_to_gold(input_table_name, data_pack_name, dataset_name, input_db_name=SILVER_DB_NAME, partition_columns=None, spark=None, write_options: dict = None,
                   processing_function=None, processing_function_args=None, processing_function_kwargs=None, profiling=False, sort_fields: list = None, upsert_fields: list = None,
                   reset_checkpoint=False):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()
    if upsert_fields is None:
        upsert_fields = ['cortex_id']
    if sort_fields is None:
        sort_fields = get_table_partitions(spark=spark, db_name=input_db_name, table_name=input_table_name)

    df = read_table(spark, db_name=input_db_name, table_name=input_table_name)
    df = apply_processing_function(df=df, func=processing_function, func_args=processing_function_args, func_kwargs=processing_function_kwargs)

    checkpoint_location = build_checkpoint_path(bucket_name=GOLD_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table_name)
    stream = write_table(df, checkpoint_location=checkpoint_location, db_name=GOLD_DB_NAME, table_name=dataset_name, spark=spark,
                         partition_columns=partition_columns, write_options=write_options, sort_fields=sort_fields, upsert_fields=upsert_fields)
    if reset_checkpoint:
        stream.awaitTermination()
        reset_autoloader_checkpoint(bucket_name=GOLD_BUCKET, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table_name)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(f'{GOLD_DB_NAME}.{dataset_name}')
        apply_profiling(df=df, data_pack_name=data_pack_name, dataset_name=dataset_name)


if __name__ == '__main__':
    data_input_path = 's3://cortex-data-platform-trusted-area-dev/salesdata/year=2022/month=04/day=22/c643c9d88fec4e39b5a7539c7ed966d7.csv'
    __list_partition_columns(data_input_path)
