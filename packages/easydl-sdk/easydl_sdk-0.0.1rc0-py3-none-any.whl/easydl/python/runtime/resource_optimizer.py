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

import traceback
from easydl.python.common.constants import EasydlOptRetriever
from easydl.python.common.log_utils import default_logger as logger
from easydl.python.runtime.easydl_client import GlobalEasydlClient


def catch_easydl_optimization_exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.warning("Fail to execute %s by %s", func.__name__, e)
            traceback.print_exc()

    return wrapper


class EDLJobResoureOptimizer(object):
    def __init__(self, job_uuid):
        self._job_uuid = job_uuid
        self._easydl_client = GlobalEasydlClient.EASYDL_CLIENT

    @catch_easydl_optimization_exception
    def get_optimization_plan(self, stage, config={}):
        res = self._easydl_client.get_optimization_plan(
            self._job_uuid,
            stage,
            EasydlOptRetriever.BASE_CONFIG_RETRIEVER,
            config,
        )
        if not res.job_optimize_plans:
            logger.info("No any optimization plan for PS")
            return

        plan = res.job_optimize_plans[0]
        logger.info("The optimization plan of %s is %s", stage, plan)
        return plan
