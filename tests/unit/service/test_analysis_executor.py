from typing import Optional
import unittest
from unittest.mock import Mock, call

from raster_analysis_service.service.analysis_executor import ProcessBasedExecutor, SequentialExecutor, get_executor_type


class GetExecutorTypeTest(unittest.TestCase):
    def test_process_base_return(self):
        executor_type = get_executor_type()
        self.assertEqual(executor_type, ProcessBasedExecutor)


class SequentialExecutorTest(unittest.TestCase):
    executor: Optional[SequentialExecutor]

    def setUp(self) -> None:
        self._analysis = Mock()
        self._dataset = ["PATH1", "PATH2"]
        self.executor = SequentialExecutor(self._analysis, self._dataset)

    def tearDown(self) -> None:
        self._analysis = None
        self._dataset = None
        self.executor = None

    def test_execute(self):
        self.executor._analyze_image = Mock()
        self.executor.execute()
        for p in self._dataset:
            self.assertTrue(call(p) in self.executor._analyze_image.call_args_list)
