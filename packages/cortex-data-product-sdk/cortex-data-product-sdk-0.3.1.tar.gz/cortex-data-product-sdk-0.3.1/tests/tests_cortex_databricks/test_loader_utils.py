from pyspark.sql.types import StructType, StructField, IntegerType, StringType

from data_product_sdk.cortex_databricks.data_platform.loader_utils import __get_partition_type, landing_to_bronze, read_table, write_table, BRONZE_DB_NAME
import logging
import pytest
from pyspark.sql import SparkSession, DataFrame


def quiet_py4j():
    """Suppress spark logging for the test context."""
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_session(request) -> SparkSession:
    """Fixture for creating a spark context."""

    spark = (SparkSession
             .builder
             .master('local[2]')
             .appName('pytest-pyspark-local-testing')
             .enableHiveSupport()
             .getOrCreate())
    request.addfinalizer(lambda: spark.stop())

    quiet_py4j()
    return spark


def test_read_table(spark_session: SparkSession) -> DataFrame:
    # prepare
    db_name = 'teste'
    table_name = 'test'
    schema = StructType([
        StructField('cortex_id', IntegerType(), True),
        StructField('label', StringType(), True),
        StructField('year', IntegerType(), True),
        StructField('month', IntegerType(), True),
        StructField('day', IntegerType(), True),
    ])

    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    spark_session.catalog.setCurrentDatabase(db_name)
    if not spark_session._jsparkSession.catalog().tableExists(db_name, table_name):
        spark_session.catalog.createTable(tableName=table_name, schema=schema)

    # execute
    df = read_table(spark_session=spark_session, db_name='teste', table_name='test')
    df.printSchema()

    # assert
    assert not set(df.schema).symmetric_difference(set(schema))
    return df


def test_write_table(spark_session: SparkSession):
    # prepare
    db_name = 'teste'
    input_table = 'input_table'
    schema = StructType([
        StructField('cortex_id', IntegerType(), True),
        StructField('label', StringType(), True),
        StructField('year', IntegerType(), True),
        StructField('month', IntegerType(), True),
        StructField('day', IntegerType(), True),
    ])
    df = spark_session.createDataFrame(
        [
            (1, "foo", 2022, 5, 1),
            (2, "bar", 2022, 5, 1),
        ],
        schema=schema
    )

    spark_session.sql(f"DROP DATABASE {db_name} CASCADE ")
    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    spark_session.catalog.setCurrentDatabase(db_name)
    df.write.format('parquet').saveAsTable(input_table, mode='append', partitionBy=['year', 'month', 'day'])

    # execute
    output_table = 'output_table'
    partition_columns = ['year', 'month', 'day']
    checkpoint_location = 'test_location/checkpoint/test'
    df = read_table(spark_session=spark_session, db_name=db_name, table_name=input_table)
    # write_table(df=df, checkpoint_location=checkpoint_location, db_name=db_name, table_name=output_table, spark=spark_session, partition_columns=partition_columns) # TODO: FALHA POIS FORMATO DELTA SO EXISTE NO DATABRICKS
    stream = df.writeStream.trigger(once=True) \
        .format('parquet') \
        .option('checkpointLocation', checkpoint_location) \

    stream.toTable(tableName=f'{db_name}.{output_table}', partitionBy=partition_columns)

    # assert
