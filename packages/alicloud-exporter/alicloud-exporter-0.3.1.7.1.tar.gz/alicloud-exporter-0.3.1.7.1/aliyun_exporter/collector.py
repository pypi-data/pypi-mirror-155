#!/bin/env python
#Add lables
import json
import yaml
import logging
import time
import os
from datetime import datetime, timedelta
from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from aliyunsdkcore.client import AcsClient
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancePerformanceRequest
from ratelimiter import RateLimiter
from aliyun_exporter.info_provider import InfoProvider
from aliyun_exporter.utils import try_or_else

rds_performance = 'rds_performance'
special_projects = {
    rds_performance: lambda collector : RDSPerformanceCollector(collector),
}

requestSummary = Summary('cloudmonitor_request_latency_seconds', 'CloudMonitor request latency', ['project'])
requestFailedSummary = Summary('cloudmonitor_failed_request_latency_seconds', 'CloudMonitor failed request latency', ['project'])

class CollectorConfig(object):
    def __init__(self,
                 pool_size=10,
                 rate_limit=10,
                 credential=None,
                 metrics=None,
                 game_name=None,
                 info_metrics=None,
                 global_config=None,
                 ):
        self.credential = credential
        self.metrics = metrics
        self.game_name = game_name
        self.rate_limit = rate_limit
        self.info_metrics = info_metrics
        self.global_config = global_config
        access_id = os.environ.get('ALIYUN_ACCESS_ID')
        access_secret = os.environ.get('ALIYUN_ACCESS_SECRET')
        region = os.environ.get('ALIYUN_REGION')
        if self.credential is None:
            self.credential = {}
        if access_id is not None and len(access_id) > 0:
            self.credential['access_key_id'] = access_id
        if access_secret is not None and len(access_secret) > 0:
            self.credential['access_key_secret'] = access_secret
        if region is not None and len(region) > 0:
            self.credential['region_id'] = region
        if self.credential['access_key_id'] is None or \
                self.credential['access_key_secret'] is None:
            raise Exception('Credential is not fully configured.')
class AliyunCollector(object):
    def __init__(self, config: CollectorConfig):
        self.metrics = config.metrics
        self.game_name = config.game_name
        self.global_config = config.global_config
        self.info_metrics = config.info_metrics
        self.client = AcsClient(
            ak=config.credential['access_key_id'],
            secret=config.credential['access_key_secret'],
            region_id=config.credential['region_id']
        )
        self.rateLimiter = RateLimiter(max_calls=config.rate_limit)
        self.info_provider = InfoProvider(self.client)
        self.special_collectors = dict()
        for k, v in special_projects.items():
            if k in self.metrics:
                self.special_collectors[k] = v(self)

    def query_metric(self, project: str, metric: str, period: int):
        with self.rateLimiter:
            req = QueryMetricLastRequest.QueryMetricLastRequest()
            req.set_Project(project)
            req.set_Metric(metric)
            req.set_Period(period)
            start_time = time.time()
            try:
                resp = self.client.do_action_with_exception(req)
            except Exception as e:
                logging.error('Error request cloud monitor api', exc_info=e)
                requestFailedSummary.labels(project).observe(time.time() - start_time)
                return []
            else:
                requestSummary.labels(project).observe(time.time() - start_time)
        data = json.loads(resp)
        func = dict()
        points = []
        [func.update(i) for a in self.game_name for i in self.game_name[a]]
        points_source = json.loads(data['Datapoints'])
        instanceid = [k for i in points_source for j in func for k,v in i.items() if v == j]
        points = [k for k in points_source for i in func if  k[instanceid[0]] == i]
        [ls.update({'name':func[dc],'region':self.global_config['region'],'app':self.global_config['app']}) for ls in points for dc in func.keys() if ls[instanceid[0]] == dc]
        [i.update({'altype':j['team'].split("-")[0],'team':j['team']}) for i in points for j in self.metrics[project] if j['name'] == metric]
        [ a.update({'cluster':dc}) for a in points for dc in self.game_name for c in self.game_name[dc] if a['instanceId'] in c ]

        return points

    def parse_label_keys(self, point):
        return [k for k in point if k not in ['timestamp', 'Maximum', 'Minimum', 'Average', 'userId', 'serviceid' , 'job', 'instance']]

    def format_metric_name(self, project, name):
        return 'aliyun_{}_{}'.format(project, name)

    def metric_generator(self, project, metric):
        if 'name' not in metric:
            raise Exception('name must be set in metric item.')
        name = metric['name']
        metric_name = metric['name']
        period = 60
        measure = 'Average'
        altype = 'email'
        if 'rename' in metric:
            name = metric['rename']
        if 'period' in metric:
            period = metric['period']
        if 'measure' in metric:
            measure = metric['measure']

        try:
            points = self.query_metric(project, metric_name, period)
        except Exception as e:
            logging.error('Error query metrics for {}_{}'.format(project, metric_name), e)
            yield metric_up_gauge(self.format_metric_name(project, name), False)
            return
        if len(points) < 1:
            yield metric_up_gauge(self.format_metric_name(project, name), False)
            return
        label_keys = self.parse_label_keys(points[0])
        gauge = GaugeMetricFamily(self.format_metric_name(project, name), '', labels=label_keys)
        for point in points:
            gauge.add_metric([try_or_else(lambda: str(point[k]), '') for k in label_keys], point[measure])
        yield gauge
        yield metric_up_gauge(self.format_metric_name(project, name), True)

    def collect(self):
        for project in self.metrics:
            if project in special_projects:
                continue
            for metric in self.metrics[project]:
                yield from self.metric_generator(project, metric)
        if self.info_metrics != None:
            for resource in self.info_metrics:
                yield self.info_provider.get_metrics(resource)
        for v in self.special_collectors.values():
            yield from v.collect()



def metric_up_gauge(resource: str, succeeded=True):
    metric_name = resource + '_up'
    description = 'Did the {} fetch succeed.'.format(resource)
    return GaugeMetricFamily(metric_name, description, value=int(succeeded))


class RDSPerformanceCollector:

    def __init__(self, delegate: AliyunCollector):
        self.parent = delegate

    def collect(self):
        for id in [s.labels['DBInstanceId'] for s in self.parent.info_provider.get_metrics('rds').samples]:
            metrics = self.query_rds_performance_metrics(id)
            for metric in metrics:
                yield from self.parse_rds_performance(id, metric)

    def parse_rds_performance(self, id, value):
        value_format: str = value['ValueFormat']
        metric_name = value['Key']
        keys = ['value']
        if value_format is not None and '&' in value_format:
            keys = value_format.split('&')
        metric = value['Values']['PerformanceValue']
        if len(metric) < 1:
            return
        values = metric[0]['Value'].split('&')
        for k, v in zip(keys, values):
            gauge = GaugeMetricFamily(
                self.parent.format_metric_name(rds_performance, metric_name + '_' + k),
                '', labels=['instanceId'])
            gauge.add_metric([id], float(v))
            yield gauge

    def query_rds_performance_metrics(self, id):
        req = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
        req.set_DBInstanceId(id)
        req.set_Key(','.join([metric['name'] for metric in self.parent.metrics[rds_performance]]))
        now = datetime.utcnow();
        now_str = now.replace(second=0, microsecond=0).strftime("%Y-%m-%dT%H:%MZ")
        one_minute_ago_str = (now - timedelta(minutes=1)).replace(second=0, microsecond=0).strftime("%Y-%m-%dT%H:%MZ")
        req.set_StartTime(one_minute_ago_str)
        req.set_EndTime(now_str)
        try:
            resp = self.parent.client.do_action_with_exception(req)
        except Exception as e:
            logging.error('Error request rds performance api', exc_info=e)
            return []
        data = json.loads(resp)
        return data['PerformanceKeys']['PerformanceKey']
