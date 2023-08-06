import json
from http import HTTPStatus

import requests
import logging

from airflow.models import Variable
from airflow.sensors.base import BaseSensorOperator

from data_product_sdk.cortex_airflow.data_platform.operators.sid_operators import SidOperator
from data_product_sdk.cortex_airflow.data_platform.utils.sid_utils import check_completed_execution_id

logger = logging.getLogger(__name__)


class SidSensor(BaseSensorOperator):
    def __init__(self, poke_interval=30, timeout=300, platform_url: str = None, username: str = None, password: str = None,
                 sid_operator: SidOperator = None, retries=20, **kwargs) -> None:
        """
        Sensor that works in conjunction with :class:`SidOperator`. It is used to monitor if SID is done loading the data into the platform

        :param poke_interval: time in seconds between API calls to SID
        :param retries: number of times to retry this task in case of failure
        :param timeout: time in seconds of sensor timeout
        :param platform_url: id of the platform to be stored the data
        :param username: platform login username
        :param password: platform login password
        :param sid_operator: SidOperator object that was used to input data, its metadata will be utilized to monitor if the data was upload successfully
        :param kwargs: all kwargs will be forwarded to the BaseSensorOperator as parameters
        """
        super().__init__(poke_interval=poke_interval, timeout=timeout, retries=retries, **kwargs)
        self.sid_operator = sid_operator
        self.platform_url = platform_url
        self.username = username
        self.password = password
        self.completed_executions = dict()

    def __check_completed_execution_ids(self, execution_ids: list, platform_url: str, username: str, password: str):
        for execution_id in execution_ids:
            response = check_completed_execution_id(execution_id=execution_id, platform_url=platform_url, username=username, password=password)
            logger.info(f'EXECUTION RESPONSE: {response}')
            completed = response['completed'] and response.get('success', False)
            self.completed_executions[execution_id] = completed
        logging.info(f'EXECUTION_IDS_COMPLETION: {self.completed_executions}')

    def check_execution_ids_completed(self, execution_ids: list, platform_url: str, username: str, password: str):
        self.__check_completed_execution_ids(execution_ids=execution_ids, platform_url=platform_url, username=username, password=password)
        return all(self.completed_executions.values())

    def poke(self, context, execution_ids=None, platform_url=None, username=None, password=None, sid_operator=None) -> bool:
        platform_url = self.platform_url if platform_url is None else platform_url
        username = self.username if username is None else username
        password = self.password if password is None else password
        sid_operator = self.sid_operator if sid_operator is None else sid_operator
        assert (execution_ids and platform_url) or (username and password and platform_url) or sid_operator, \
            'You need to pass a execution_id platform_url or a sid_operator as valid parameters'

        if execution_ids and platform_url and username and password:
            completed = self.check_execution_ids_completed(execution_ids=execution_ids, platform_url=platform_url, username=username, password=password)
            return completed
        elif sid_operator is not None:
            execution_ids = context['task_instance'].xcom_pull(task_ids=sid_operator.task_id, key='execution_ids')
            platform_url = context['task_instance'].xcom_pull(task_ids=sid_operator.task_id, key='platform_url')
            credentials = context['task_instance'].xcom_pull(task_ids=sid_operator.task_id, key='credentials')
            username = credentials['username']
            password = credentials['password']
            if sid_operator.ignore_empty_dataframe and not execution_ids and not platform_url:
                logging.info('ACCEPTING EMPTY DATAFRAME')
                return True

        logging.info(f'POKE:\n EXECUTION IDS: {execution_ids}')
        completed = self.check_execution_ids_completed(execution_ids=execution_ids, platform_url=platform_url, username=username, password=password)

        return completed
