from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3
import data_product_sdk.cortex_databricks.data_platform.loader_utils as loader_utils


def reset_autoloader_checkpoint(bucket_name, data_pack_name, dataset_name, input_table_name='', region_name='us-east-1'):
    s3_client = S3(bucket_name=bucket_name, region_name=region_name)
    checkpoint_location = loader_utils.build_checkpoint_path(bucket_name=bucket_name, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table_name)
    print('DELETING CHECKPOINT: ', checkpoint_location)
    s3_bucket, s3_key = s3_client.get_bucket_key_from_s3_url(s3_url=checkpoint_location)

    return s3_client.delete_files(prefix=s3_key)


if __name__ == '__main__':
    bucket_name = 'cortex-databricks-gold-dev'
    input_table = 'testes_upsert'
    data_pack_name = 'testes'
    dataset_name = 'testes_upsert'

    reset_autoloader_checkpoint(bucket_name='cortex-databricks-gold-dev', data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name=input_table)
