import os
from itertools import chain

import pyspark.sql.functions as F
from delta import DeltaTable
from pyspark.sql import SparkSession, Column

ENVIRONMENT = os.getenv('ENVIRONMENT', default='dev')


def get_spark_session(app_name: str):
    """
    Obtain a :class:`SparkSession` with the corresponding appName

    :param app_name:
    :return: SparkSession object with the session
    """
    spark = SparkSession \
        .builder \
        .config("spark.hadoop.hive.exec.dynamic.partition", "true") \
        .config("spark.hadoop.hive.exec.dynamic.partition.mode", "nonstrict") \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .enableHiveSupport() \
        .appName(app_name) \
        .getOrCreate()

    return spark


def apply_mapping_to_column(col: Column, mapping: dict) -> Column:
    """
    Receives a :class:`Column` and a :class:`dict` and returns a :class:`Column` mapped to the mapping dictionary
    This operation is executed purely on spark java code, and should be prefered over using python UDFs

    :param col: Column to be mapped
    :param mapping: Dictionary that will apply to the Column
    :return: Column with the dictionary applied the mapping
    """
    mapping_expr = F.create_map([F.lit(x) for x in chain(*mapping.items())])
    return mapping_expr[col]

def check_table_exists(db_name: str, table_name: str, spark: SparkSession = None):
    """
    Check if the the corresponding table existis on the database
    :param db_name:
    :param table_name:
    :param spark:
    :return:
    """
    if spark is None:
        spark = get_spark_session('check_table_exists')

    return spark._jsparkSession.catalog().tableExists(db_name, table_name)


def get_table_partitions(db_name: str, table_name: str, spark: SparkSession = None):
    if spark is None:
        spark = get_spark_session('get_table_partitions')

    return spark.sql(f"SHOW Partitions {db_name}.{table_name}").columns


def build_matching_sort_condition(sort_fields: list, existing_df_name='target', inserting_df_name='source'):
    match_condition = None
    for field in sort_fields:
        compare_symbol = '<' if field == sort_fields[-1] else '<='
        if field == sort_fields[0]:
            match_condition = f'{existing_df_name}.{field} {compare_symbol} {inserting_df_name}.{field} '
        else:
            match_condition = f'{match_condition} AND {existing_df_name}.{field} {compare_symbol} {inserting_df_name}.{field} '

    return match_condition


def drop_table_duplicates(db_name: str, table_name: str, unique_id_fields: list = None, sort_fields: list = None, spark: SparkSession = None):
    if spark is None:
        spark = get_spark_session(f'drop_duplicates_{db_name}.{table_name}')
    if not unique_id_fields:
        unique_id_fields = ['cortex_id']
    if sort_fields is None:
        sort_fields = get_table_partitions(spark=spark, db_name=db_name, table_name=table_name)
    existing_table_alias = 'target'
    inserting_table_alias = 'source'

    for field in unique_id_fields:
        unique_condition = f'{inserting_table_alias}.{field} = {existing_table_alias}.{field} '  # TODO: FUNCIONA APENAS COM UMA
    match_condition = build_matching_sort_condition(sort_fields=sort_fields, existing_df_name=existing_table_alias, inserting_df_name=inserting_table_alias)

    unique_id_fields = ','.join(unique_id_fields)
    sort_fields = ','.join(sort_fields)
    db_table = f'{db_name}.{table_name}'

    df_last_sort = spark.sql(f"""
        select * from (
            select *, ROW_NUMBER() OVER (Partition By {unique_id_fields} Order By {sort_fields} desc) as rn
            from {db_table} t1
            )
        where rn = 1
    """)
    existing_table = DeltaTable.forName(spark, db_table)
    existing_table.alias(existing_table_alias).merge(df_last_sort.alias(inserting_table_alias), unique_condition). \
        whenMatchedDelete(match_condition). \
        execute()
