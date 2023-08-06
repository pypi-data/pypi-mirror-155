import sys

import uuid

import pyspark.sql.functions as F
import unicodedata
from pyspark.sql import Column

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StringType
from pyspark.sql.utils import AnalysisException

from data_product_sdk.cortex_databricks.data_platform.schema_utils import get_schema_from_s3
from data_product_sdk.cortex_databricks.data_platform.spark_utils import get_spark_session


def remove_excess_spaces(col: Column):
    return F.regexp_replace(col, r'\\s+', '')


def remove_accents(col: Column):
    matching_string = ""
    replace_string = ""

    for i in range(ord(" "), sys.maxunicode):
        name = unicodedata.name(chr(i), "")
        if "WITH" in name:
            try:
                base = unicodedata.lookup(name.split(" WITH")[0])
                matching_string += chr(i)
                replace_string += base
            except KeyError:
                pass

    return F.translate(
        F.regexp_replace(col, r"\p{M}", ""),
        matching_string, replace_string
    )


def __apply_case(col: Column, case=None):
    if case == 'upper':
        col = F.upper(col)
    elif case == 'lower':
        col = F.lower(col)
    elif case == 'root_cnpj':
        col = __treat_document(col, 8)
    elif case == 'cnpj':
        col = __treat_document(col, 14)
    elif case == 'cpf':
        col = __treat_document(col, 11)
    elif case == 'cep':
        col = __treat_document(col, 8)

    return col


def __treat_document(col: Column, doc_size: int):
    col = F.regexp_replace(col, r'[^0-9]', '')
    col = F.lpad(col, doc_size, '0')

    null_doc = ''.zfill(doc_size) # like 00000000
    col = F.when(col != null_doc, col).otherwise('')

    return col


def __apply_metadata(col: Column, metadata=None):
    if metadata:
        col = col.alias("", metadata=metadata)
    return col


def __apply_date_format(col: Column, date_format=None):
    if date_format:
        col = F.to_date(col, format=date_format)
    return col


def __apply_timestamp_format(col: Column, timestamp_format=None):
    if timestamp_format:
        col = F.to_timestamp(col, format=timestamp_format)
    return col


def process_string_column(col: Column, column_metadata: dict):
    case = column_metadata.get('case')
    date_format = column_metadata.get('date_format')
    timestamp_format = column_metadata.get('timestamp_format')

    # parametrizados
    col = __apply_case(col, case=case)
    col = __apply_date_format(col, date_format=date_format)
    col = __apply_timestamp_format(col, timestamp_format=timestamp_format)

    # obrigatorios
    col = remove_accents(col)
    col = remove_excess_spaces(col)

    # reaplicando metadata
    col = __apply_metadata(col, metadata=column_metadata)

    return col


def __get_metadata_from_schema(schema, metadata: dict = None, prefix=''):
    if metadata is None:
        metadata = dict()

    fields = schema['fields']
    for field in fields:
        if not isinstance(field['type'], dict) or field['type'].get('type') != 'struct':
            field_name = prefix + field['name']
            metadata[field_name] = field['metadata']
        else:
            __get_metadata_from_schema(schema=field['type'], metadata=metadata, prefix=f"{prefix}{field['name']}.")

    return metadata


def get_column_type(df: DataFrame, column_name: str):
    return df.select(column_name).schema.fields[0].dataType


def process_dataframe(df: DataFrame, js_schema: dict):
    if js_schema is None:
        return df

    metadatas = __get_metadata_from_schema(js_schema)
    print(f'METADATAS: {metadatas}')

    for column_name, column_metadata in metadatas.items():
        # print(column_name, column_metadata)
        try:
            column_type = get_column_type(df, column_name)
        except AnalysisException:
            continue  # skip columns on the schema that are not on the data

        if isinstance(column_type, StringType):
            columns = iter(column_name.split('.', maxsplit=1))
            father_column = next(columns, None)
            child_column = next(columns, None)

            processed_column = process_string_column(df[column_name], column_metadata=column_metadata)
            if child_column:
                df = df.withColumn(father_column, df[father_column].withField(child_column, processed_column))
            else:
                df = df.withColumn(column_name, processed_column)

        rename = column_metadata.get('rename')
        if rename:
            df = df.withColumnRenamed(column_name, rename)
            column_name = rename

    return df


def create_cortex_id(df: DataFrame, key_columns: list = None):
    if key_columns is None:
        return df

    print('keys to generate cortex_id:', key_columns)
    metadata = {
        'comment': 'Cortex unique id'
    }

    df = df.select(F.concat_ws("-", *[F.col(x) for x in key_columns]).alias("cortex_id"),"*")
    df = df.withColumn('cortex_id', F.md5(df.cortex_id).alias("", metadata=metadata))
    return df


if __name__ == '__main__':
    schema_path = 's3://cortex-databricks-bronze-dev/_schemas/emails_schema.json'
    js_schema = get_schema_from_s3(schema_path)
    spark = get_spark_session('teste')
    df = spark.read.parquet('../../receita_federal/bronze_layer/cities.parquet')
    df.printSchema()
    df.show(5)

    df = process_dataframe(df, js_schema=js_schema)
    df.printSchema()
    df.show(5)
