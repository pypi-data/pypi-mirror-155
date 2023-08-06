import base64
import json
import os
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError

DEFAULT_REGION = 'us-east-1'


class DataBrewClient:
    def __init__(self):
        self.client = boto3.client('databrew', region_name='us-east-1')

    def start_databrew_profiling_job(self, job_name):
        response = self.client.start_job_run(
            Name=job_name
        )

        return response


class S3:
    def __init__(self, bucket_name, region_name=DEFAULT_REGION):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            region_name=region_name
        )

    @staticmethod
    def build_s3_uri(s3_bucket: str, s3_key: str):
        return f's3://{s3_bucket}/{s3_key}'

    @staticmethod
    def get_bucket_key_from_s3_url(s3_url):
        url = urlparse(s3_url, allow_fragments=False)
        s3_bucket, s3_key = url.netloc, url.path.lstrip('/')

        return s3_bucket, s3_key

    def upload_s3_file(self, path, s3_key, meta_tags=None):
        if meta_tags is None:
            meta_tags = dict()
        extra_args = {"Metadata": meta_tags}
        self.s3_client.upload_file(path, self.bucket_name, s3_key, ExtraArgs=extra_args)

    def download_s3_file(self, s3_path, path):
        self.s3_client.download_file(self.bucket_name, s3_path, path)

    def delete_file(self, s3_path):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_path)

    def delete_files(self, prefix):
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
            if result.get('Contents') is not None:
                for file in result.get('Contents'):
                    self.delete_file(s3_path=file['Key'])

    def list_s3_files(self, prefix='', delimiter=''):
        paginator = self.s3_client.get_paginator('list_objects_v2')
        files = dict()
        for result in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix, Delimiter=delimiter):
            if not files:
                files = result
            else:
                files['Contents'].extend(result.get('Contents', []))
        return files.get('Contents')

    def upload_file_obj(self, file_obj, s3_key, s3_additional_kwargs=None):
        if s3_additional_kwargs is None:
            s3_additional_kwargs = dict()
        self.s3_client.upload_fileobj(Fileobj=file_obj, Bucket=self.bucket_name, Key=s3_key, **s3_additional_kwargs)

    def put_object(self, data, s3_key, s3_additional_kwargs=None):
        if s3_additional_kwargs is None:
            s3_additional_kwargs = dict()
        self.s3_client.put_object(Body=data, Bucket=self.bucket_name, Key=s3_key, **s3_additional_kwargs)

    def get_object(self, s3_path):
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_path)
        return obj['Body']

    def download_dir(self, prefix, local=None):
        if local is None:
            local = os.getcwd()
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=self.bucket_name, Delimiter='/', Prefix=prefix):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    self.download_dir(subdir.get('Prefix'), local)
            if result.get('Contents') is not None:
                directory = result.get('Contents')[0]['Key']
                if not os.path.exists(os.path.dirname(local + os.sep + directory)):
                    os.makedirs(os.path.dirname(local + os.sep + directory))
                for file in result.get('Contents'):
                    self.s3_client.download_file(self.bucket_name, file.get('Key'), local + os.sep + file.get('Key'))

    def generate_presigned_url(self, bucket, key, method='put_object', expires_in=300):
        self.s3_client.generate_presigned_url(method, Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires_in)


class SecretsManager:
    def __init__(self, secret_name, region_name=DEFAULT_REGION):
        if region_name == None:
            region_name = 'us-east-1'
        session = boto3.session.Session()
        self.client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        self.secret_name = secret_name

    def get_secret(self):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secrets = json.loads(get_secret_value_response['SecretString'])
                return secrets
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return decoded_binary_secret


class SQS:
    def __init__(self, queue_url, region_name=DEFAULT_REGION, client=None):
        self.queue_url = queue_url
        self.sqs_client = client
        if client is None:
            self.sqs_client = SQS.gen_client(region_name=region_name)

    @staticmethod
    def gen_client(region_name=DEFAULT_REGION):
        client = boto3.client(
            'sqs',
            region_name=region_name
        )
        return client

    @classmethod
    def from_queue_name(cls, queue_name, region_name=DEFAULT_REGION):
        client = SQS.gen_client(region_name=region_name)
        queue_url = client.get_queue_url(QueueName=queue_name)
        queue_url = queue_url['QueueUrl']
        return cls(queue_url=queue_url, client=client)

    def put_on_queue(self, message, message_attributes={}):
        response = self.sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message,
            MessageAttributes=message_attributes,
        )
        return response

    def get_from_queue(self):
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            WaitTimeSeconds=5
        )
        try:
            message = response['Messages'][0]
        except KeyError:
            return None, None
        return json.loads(message['Body']), message['ReceiptHandle']

    def get_queue_size(self):
        n_messages = self.sqs_client.get_queue_attributes(QueueUrl=self.queue_url, AttributeNames=['ApproximateNumberOfMessages'])
        return int(n_messages['Attributes']['ApproximateNumberOfMessages'])

    def delete_from_queue(self, receipt_handle):
        self.sqs_client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)

    def purge_queue(self):
        self.sqs_client.purge_queue(QueueUrl=self.queue_url)


class DynamoDB:
    def __init__(self, table_name, region_name=DEFAULT_REGION):
        self.dynamo_db = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamo_db.Table(table_name)

    def put_item(self, item):
        response = self.table.put_item(Item=item)
        return response

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response['Item']

    def update_item(self, key, update_values):
        update_expression = {k: f":{k.split('.')[-1]}" for k, v in update_values.items()}
        expression_values = {v: update_values[k] for k, v in update_expression.items()}
        update_expression = 'set ' + ','.join([f'{k}={v}' for k, v in update_expression.items()])
        response = self.table.update_item(Key=key,
                                          UpdateExpression=update_expression,
                                          ExpressionAttributeValues=expression_values,
                                          ReturnValues="UPDATED_NEW"
                                          )
        return response

    def query(self, expression):
        response = self.table.query(IndexName='s3_bucket-s3_key-index',
                                    KeyConditionExpression=expression
                                    )
        return response['Items']

    def get_all(self):
        res = self.table.scan()
        data = res['Items']

        while res.get('LastEvaluatedKey'):
            response = self.table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
            data.extend(response['Items'])

        return data


if __name__ == '__main__':
    s3_client = S3(bucket_name='cortex-data-platform-trusted-area-dev')
    s3_client.download_dir(prefix='receita_federal/dados_abertos_cnpj/empresas/year=2022/month=02/day=15/')