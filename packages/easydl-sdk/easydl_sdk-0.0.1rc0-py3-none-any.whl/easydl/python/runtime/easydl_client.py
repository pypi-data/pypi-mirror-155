# Copyright 2020 The ElasticDL Authors. All rights reserved.
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

import os

from easydl.proto import easydl_pb2, easydl_pb2_grpc
from elasticai_api.util.grpc_utils import build_channel
from elasticai_api.util.log_utils import default_logger as logger

EASYDL_BRAIN_ADMINISTER_ADDR = "easydl-brain-administer.kubemaker.svc.\
em14.alipay.com:50001"
EASYDL_BRAIN_PROCESSOR_ADDR = "easydl-brain-processor.kubemaker.svc.\
em14.alipay.com:50001"
DATA_STORE = "data_store_elasticdl"
OPTIMIZE_PROCESSOR = "running_training_job_optimize_processor"


def catch_exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.warning(
                "Fail to %s.%s by %s",
                self.__class__.__name__,
                func.__name__,
                e,
            )

    return wrapper


def init_job_metrics_message(job_uuid):
    job_metrics = easydl_pb2.JobMetrics()
    job_metrics.data_store = DATA_STORE
    job_metrics.job_meta.uuid = job_uuid
    return job_metrics


class EasydlClient(object):
    """EasyClient provides APIs to access EasyDL service via gRPC calls.

    Usage:
        channel = elasticai_api.util.grpc_utils.build_channel(
            "localhost:50001"
        )
        easydl_client = EasydlClient((channel, job_name="test")
        # Report metrics to EasyDL server
        easydl_client.report(...)
    """

    def __init__(self, administer_channel, processor_channel):
        """Initialize an EasyDL client.
        Args:
            channel: grpc.Channel
            the gRPC channel object connects to master gRPC server.

            job_name: string
            the unique and ordered worker ID assigned
            by elasticdl command-line.
        """
        self._administer_stub = easydl_pb2_grpc.EasyDLStub(administer_channel)
        self._processor_stub = easydl_pb2_grpc.OptimizeProcessorStub(
            processor_channel
        )

    def report_metrics(self, job_metrics):
        """Report job metrics to administer service"""
        return self._administer_stub.persist_metrics(job_metrics)

    def get_job_metrics(self, job_uuid):
        """Get the job metrics by the job uuid.
        Examples:
            ```
            import json

            client = build_easydl_client()
            metrics_res = client.get_job_metrics("xxxx")
            metrics = json.loads(metrics_res.job_metrics)
            ```
        """
        request = easydl_pb2.JobMetricsRequest()
        request.job_uuid = job_uuid
        return self._administer_stub.get_job_metrics(request)

    def request_optimization(self, opt_request):
        """Get the optimization plan from the processor service"""
        logger.info("Optimization request is %s", opt_request)
        return self._processor_stub.optimize(opt_request)

    def report_training_hyper_params(self, job_uuid, hyper_params):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Training_Hyper_Params
        metrics = job_metrics.training_hyper_params
        metrics.batch_size = hyper_params.batch_size
        metrics.epoch = hyper_params.epoch
        metrics.max_steps = hyper_params.max_steps
        return self.report_metrics(job_metrics)

    def report_workflow_feature(self, job_uuid, workflow_feature):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.job_meta.name = workflow_feature.job_name
        job_metrics.job_meta.user = workflow_feature.user_id
        job_metrics.metrics_type = easydl_pb2.MetricsType.Workflow_Feature

        metrics = job_metrics.workflow_feature
        metrics.job_name = workflow_feature.job_name
        metrics.user_id = workflow_feature.user_id
        metrics.code_address = workflow_feature.code_address
        metrics.workflow_id = workflow_feature.workflow_id
        metrics.node_id = workflow_feature.node_id
        metrics.odps_project = workflow_feature.odps_project
        metrics.is_prod = workflow_feature.is_prod
        return self.report_metrics(job_metrics)

    def report_training_set_metric(self, job_uuid, dataset_metric):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Training_Set_Feature
        metrics = job_metrics.training_set_feature
        metrics.dataset_size = dataset_metric.dataset_size
        metrics.dataset_name = dataset_metric.dataset_name
        sparse_features = dataset_metric.sparse_features
        metrics.sparse_item_count = sparse_features.item_count
        metrics.sparse_features = ",".join(sparse_features.feature_names)
        metrics.sparse_feature_groups = ",".join(
            [str(i) for i in sparse_features.feature_groups]
        )
        metrics.sparse_feature_shapes = ",".join(
            [str(i) for i in sparse_features.feature_shapes]
        )
        metrics.dense_features = ",".join(
            dataset_metric.dense_features.feature_names
        )
        metrics.dense_feature_shapes = ",".join(
            [str(i) for i in dataset_metric.dense_features.feature_shapes]
        )
        metrics.storage_size = dataset_metric.storage_size
        return self.report_metrics(job_metrics)

    def report_model_feature(self, job_uuid, tensor_stats, op_stats):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Model_Feature
        metrics = job_metrics.model_feature
        metrics.variable_count = tensor_stats.variable_count
        metrics.total_variable_size = tensor_stats.total_variable_size
        metrics.max_variable_size = tensor_stats.max_variable_size
        metrics.kv_embedding_dims.extend(tensor_stats.kv_embedding_dims)
        metrics.tensor_alloc_bytes.update(tensor_stats.tensor_alloc_bytes)
        metrics.op_count = op_stats.op_count
        metrics.update_op_count = op_stats.update_op_count
        metrics.read_op_count = op_stats.read_op_count
        metrics.input_fetch_dur = op_stats.input_fetch_dur
        metrics.flops = op_stats.flops
        metrics.recv_op_count = op_stats.recv_op_count
        return self.report_metrics(job_metrics)

    def report_runtime_info(self, job_uuid, namespace, runtime_metric):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Runtime_Info
        metrics = job_metrics.runtime_info
        metrics.global_step = runtime_metric.global_step
        metrics.time_stamp = runtime_metric.timestamp
        metrics.speed = runtime_metric.speed
        for pod in runtime_metric.running_pods:
            pod_meta = easydl_pb2.PodMeta()
            pod_meta.pod_name = pod.name
            pod_meta.pod_ip = pod.pod_ip
            pod_meta.node_ip = pod.node_ip
            pod_meta.host_name = pod.host_name
            pod_meta.namespace = namespace
            pod_meta.is_mixed = pod.qos == "SigmaBestEffort"
            pod_meta.mem_usage = pod.mem_usage
            pod_meta.cpu_usage = pod.cpu_usage
            metrics.running_pods.append(pod_meta)
        return self.report_metrics(job_metrics)

    def get_optimization_plan(self, job_uuid, stage, opt_retriever, config={}):
        request = easydl_pb2.OptimizeRequest()
        request.type = stage
        request.config.optimizer_config_retriever = opt_retriever
        request.config.data_store = DATA_STORE
        request.config.brain_processor = OPTIMIZE_PROCESSOR
        for key, value in config.items():
            request.config.customized_config[key] = value
        request.jobs.add()
        request.jobs[0].uid = job_uuid
        return self.request_optimization(request)

    def report_job_exit_reason(self, job_uuid, reason):
        job_metrics = init_job_metrics_message(job_uuid)
        job_metrics.metrics_type = easydl_pb2.MetricsType.Job_Exit_Reason
        job_metrics.job_exit_reason = reason
        return self.report_metrics(job_metrics)

    @catch_exception
    def get_config(self, key):
        request = easydl_pb2.ConfigRequest()
        request.config_key = key
        response = self._administer_stub.get_config(request)
        if response.response.success:
            return response.config_value
        return None


def build_easydl_client():
    """Build a client of the EasyDL server.

    Example:
        ```
        import os
        os.environ["EASYDL_BRAIN_ADMINISTER_ADDR"] = "xxx"
        client = build_easydl_client()
        ```
    """
    easydl_administer_addr = os.getenv(
        "EASYDL_BRAIN_ADMINISTER_ADDR", EASYDL_BRAIN_ADMINISTER_ADDR
    )
    administer_channel = build_channel(easydl_administer_addr)
    easydl_processor_addr = os.getenv(
        "EASYDL_BRAIN_PROCESSOR_ADDR", EASYDL_BRAIN_PROCESSOR_ADDR
    )
    processor_channel = build_channel(easydl_processor_addr)
    return EasydlClient(administer_channel, processor_channel)


class GlobalEasydlClient(object):
    EASYDL_CLIENT = build_easydl_client()
