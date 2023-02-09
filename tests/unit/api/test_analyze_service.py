import unittest
from typing import Optional
from unittest.mock import Mock, call, patch

from raster_analysis_service.service.analyze_service import AnalyzeService
from raster_analysis_service.image.analysis import AnalysisType


class AnalyzeServiceTest(unittest.TestCase):
    service: Optional[AnalyzeService]

    def setUp(self) -> None:
        self.service = AnalyzeService()

    def tearDown(self) -> None:
        self.service = None

    def test_supported_operations(self):
        supported_operations = self.service.supported_operations()

        for supported_operation in supported_operations:
            AnalysisType[supported_operation]

    @patch("raster_analysis_service.service.analyze_service.create_tif_dataset")
    def test_analyze(self, mock_create_dataset):
        paths = ["PATH1", "PATH2"]
        mock_create_dataset.return_value = paths
        self.service._analyze_image = Mock()

        self.service.analyze(AnalysisType.MEAN_VALUE)
        for p in paths:
            self.assertTrue(call(p) in self.service._analyze_image.call_args_list)
