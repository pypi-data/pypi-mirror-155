# Copyright 2022 The ElasticDL Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from easydl.proto import easydl_pb2
from easydl.python.runtime.easydl_client import (
    GlobalEasydlClient,
    init_job_metrics_message,
)


class TaskResource(object):
    def __init__(self, num=None, cpu=None, memory=None, gpu=None, rdma=None):
        self.num = num
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.rdma = rdma


class JobResource(object):
    def __init__(self, worker_resource=None, ps_resource=None):
        self.worker = worker_resource
        self.ps = ps_resource

    def to_json(self):
        data = {}
        if self.worker:
            data["worker"] = json.dumps(self.worker.__dict__)
        if self.ps:
            data["ps"] = json.dumps(self.ps.__dict__)
        return json.dumps(data)


class MetricCollector(object):
    def __init__(self):
        self._easydl_client = GlobalEasydlClient.EASYDL_CLIENT

    def report_job_meta(self, job_uuid, job_name, user_id):
        """Report the job meta to EasyDL DB.
        Args:
            job_uuid: str, the unique id of the job which is usually
                the uuid in the job yaml of k8s.
            job_name: str, the name of training job.
            user_id: the user id.
        """
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.job_meta.name = job_name
        job_metrics.job_meta.user = user_id
        job_metrics.metrics_type = easydl_pb2.MetricsType.Workflow_Feature
        metrics = job_metrics.workflow_feature
        metrics.job_name = job_name
        metrics.user_id = user_id
        self._easydl_client.report_metrics(job_metrics)

    def report_job_type(self, job_uuid, job_type):
        """Report the job type to EasyDL DB.
        Args:
            job_uuid: str, the unique id of the job which is usually
                the uuid in the job yaml of k8s.
            job_type: str, the type of training job like "alps", "atorch",
                "penrose" and so on.
        """
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Type
        job_metrics.type = job_type
        self._easydl_client.report_metrics(job_metrics)

    def report_job_resource(self, job_uuid, job_resource):
        """Report the job resource to EasyDL DB.
        Args:
            job_uuid: str, the unique id of the job which is usually
                the uuid in the job yaml of k8s.
            job_resource: JobResource instance.
        """
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Resource
        job_metrics.resource = job_resource.to_json()
        self._easydl_client.report_metrics(job_metrics)

    def report_model_meta(
        self, job_uuid, model_size=0, variable_count=0, ops_count=0
    ):
        """Report the model meta to EasyDL DB.
        Args:
            job_uuid: str, the unique id of the job which is usually
                the uuid in the job yaml of k8s.
            model size: int, the size of the NN model.
            variable_count: int, the total count of variables in the model.
            ops_count: int, the total count of ops in the model.
        """
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Model_Feature
        metrics = job_metrics.model_feature
        metrics.total_variable_size = model_size
        metrics.variable_count = variable_count
        metrics.op_count = ops_count
        self._easydl_client.report_metrics(job_metrics)

    def report_customized_data(self, job_uuid, cutomized_data):
        """Report the job resource to EasyDL DB.
        Args:
            job_uuid: str, the unique id of the job which is usually
                the uuid in the job yaml of k8s.
            cutomized_data: A dictionary.
        """
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Customized_Data
        job_metrics.customized_data = json.dumps(cutomized_data)
        self._easydl_client.report_metrics(job_metrics)
