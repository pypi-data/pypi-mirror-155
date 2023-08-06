"""Main module."""
import logging
from datetime import datetime, timedelta
from unittest import result
from influxdb_client import InfluxDBClient, Point, WritePrecision, QueryApi
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import requests
import urllib3
urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Log2Influx(object):
    def __init__(self, conf:dict) -> None:
        """This utility only supports InfluxDB 2.x.

        Args:
            conf is dict contains following info
            url: server url
            org (str): org
            token (str): access token
            bucket (str): bucket to read and write
        """
        self.url = conf["url"]
        self.org = conf["org"]
        self.token = conf["token"]
        self.bucket = conf["bucket"]
        self.app_id = conf["app_id"]

        self.token = f"Token {self.token}"
        self.header = {"Authorization": self.token, "Accept":"application/json"}
        self.param = {
            "bucket":self.bucket,
            "precision":"ns",
            "org":self.org
        }

        # self.connect()

    # Calling destructor
    # def __del__(self):
    #     logger.info("Log2Influx Destructor called")
    #     try:
    #         self.client.close()
    #         del self.client
    #     except Exception:
    #         pass

    # def connect(self):
    #     logger.info(f"connect to influxdb: {self.url} {self.org} {self.bucket}")
    #     self.client = InfluxDBClient(
    #         url="https://influxdb.swarm.edmonton.ca", token=self.token, org=self.org
    #     )
    #     self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def format_kv(self,data:dict):
        arr = []
        for k, v in data.items():
            str = f"{k}={v}"
            arr.append(str)
        
        ret = ",".join(arr)
        return ret

    # https://docs.influxdata.com/influxdb/v2.2/reference/syntax/line-protocol/
    def push_metrics(
        self,
        measurement: str,
        tags: dict,
        metrics: dict,
        time: datetime = datetime.utcnow(),
    ):
        """fucntion to store metrics

        Args:
            measurement (str): name of measurement. Same as table in RDBMS
            tags (dict): tags. Same as column in RDBMS
            metrics (dict): Store as Influxdb field. most of them are numbers.
            time (datetime, optional): timestamp. Defaults to datetime.utcnow().

        Returns:
            _type_: _description_
        """

        str_tags = self.format_kv(tags)
        str_metrics = self.format_kv(metrics)
        line_data = f'{measurement},{str_tags} {str_metrics}'
        
        ret = 0
        try:
            url = f'{self.url}/api/v2/write'
            response = requests.post(url, params=self.param,
                data=line_data, headers=self.header,
                verify=False)
            if response.status_code != 204:
                # failed
                ret = response.status_code
                logger.error(response.text)
        except Exception as ex:
            # if ex.response.status == 401:
            logger.error(ex)
            ret = 1

        return ret

    def event_login(self, user):
        tags = {"app_id": self.app_id, "user": user}
        metrics = {"count": 1.0}
        self.push_metrics("login", tags, metrics)

    def event_status_update(self, user):
        logger.debug(f"event_status_update(self, {user}):")
        tags = {"app_id": self.app_id, "user": user}
        metrics = {"count": 1.0}
        self.push_metrics("active_users", tags, metrics)

    def event_logout(self, user):
        tags = {"app_id": self.app_id, "user": user}
        metrics = {"count": 1.0}
        self.push_metrics("logout", tags, metrics)

    def event_data_load(self, user=None, success=True,elapse=None):
        tags = {"app_id": self.app_id, "user": user}
        if success is True:
            metrics = {"success": 1.0,"elapsed_time":elapse}
        else:
            metrics = {"failure": 1.0,"elapsed_time":elapse}

        self.push_metrics("data_load", tags, metrics)
        self.metrics_response_time("data_load", user=user,elapse=elapse)

    def event_others(self, event_name, user=None, metrics=None):
        tags = {"app_id": self.app_id, "user": user}
        if metrics is None:
            metrics = {"count", .0}

        self.push_metrics(event_name, tags, metrics)

    def metrics_response_time(self, metric_name, user=None, elapse=None):
        tags = {"app_id": self.app_id, "user": user,"metric":metric_name}
        metrics = {"elapsed_time": elapse}

        self.push_metrics("response_time", tags, metrics)

    def log(self, log_level:int, message:str)->int:
        """Log information to std output and influxdb2

        Args:
            log_level (int): same as pythong logging. e.g.
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0
            debug info won't write to influx db
            message (str): message to log. Don't output very long text in here.

        Returns:
            int:  0 no error 1: has error
        """

        logger.log(level=log_level,msg=message)
        if log_level == logging.DEBUG:
            # debug info won't write to influxdb2
            return 0

        line_data = f'logging,app_id={self.app_id},log_level={log_level} count=1.0,message="{message}"'
        ret = 0
        try:
            url = f'{self.url}/api/v2/write'
            response = requests.post(url, params=self.param,
                data=line_data, headers=self.header,
                verify=False)
            if response.status_code != 204:
                # failed
                ret = response.status_code
                logger.error(response.text)
        except Exception as ex:
            # if ex.response.status == 401:
            logger.error(ex)
            ret = 1

        return ret

    def delete_data(
        self,
        measurement: str = None,
        start: str = "1970-01-01T00:00:00Z",
        stop: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        ):
        """This function clear out data for a measurement/table.

        Args:
            measurement (str): measurement name

            start (str, optional): isoformat datetime. Defaults to "1970-01-01T00:00:00Z".
            stop (str, optional): isoformat datetime. Defaults to datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        """
        if measurement is None:
            data = {
                "start": start,
                "stop": stop
            }
        else:
            data = {
                # "predicate": "tag1=\"value1\" and (tag2=\"value2\" and tag3!=\"value3\")",
                "start": start,
                "stop": stop,
                "_measurement": measurement
            }

        ret = 0
        try:
            url = f'{self.url}/api/v2/delete'
            response = requests.post(url, params=self.param,
                json=data, headers=self.header,
                verify=False)
            if response.status_code != 204:
                # failed
                ret = response.status_code
                logger.error(response.text)
        except Exception as ex:
            # if ex.response.status == 401:
            logger.error(ex)
            ret = 1

        return ret

    # query examples
    # https://github.com/influxdata/influxdb-client-python/blob/master/examples/query.py
    def get_query_api(self) -> QueryApi:
        """The function return Influxdb query api.
            Because the query is very flexible,
            this util does not wrap the query funciton for you.
            please reference to this example to write your own query.
            https://github.com/influxdata/influxdb-client-python/blob/master/examples/query.py

        Returns:
            QueryApi: influxdb queery api
        """

        return self.client.query_api()
