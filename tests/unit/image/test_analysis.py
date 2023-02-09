import numpy as np
import unittest

from typing import Optional
from unittest.mock import Mock

from raster_analysis_service.image.analysis import AnalysisType, get_analysis, MeanValueAnalysis


class MeanValueAnalysisTest(unittest.TestCase):
    analysis: Optional[MeanValueAnalysis]

    def setUp(self) -> None:
        self.analysis = MeanValueAnalysis()

    def tearDown(self) -> None:
        self.analysis = None

    def test_initial_values(self):
        self.assertEqual(self.analysis.pixel_count.value, 0)
        self.assertEqual(self.analysis.average_mean.value, 0)

    def test_add(self):
        mock_raster = Mock()
        mock_raster.array.return_value = np.ones((3, 5, 5))
        self.analysis.add(mock_raster)

        self.assertEqual(self.analysis.pixel_count.value, 75)
        self.assertEqual(self.analysis.average_mean.value, 1)

    def test_add_two_images(self):
        mock_raster = Mock()
        mock_raster.array.return_value = np.ones((3, 5, 5))
        self.analysis.add(mock_raster)
        mock_raster.array.return_value = np.ones((3, 5, 5)) * 5
        self.analysis.add(mock_raster)

        self.assertEqual(self.analysis.pixel_count.value, 150)
        self.assertEqual(self.analysis.average_mean.value, 3)


class GetAnalysisTest(unittest.TestCase):
    def test_success_with_enum(self):
        analysis = get_analysis(AnalysisType.MEAN_VALUE)

        self.assertEqual(analysis, MeanValueAnalysis)

    def test_success_with_string(self):
        analysis = get_analysis(AnalysisType.MEAN_VALUE.value)

        self.assertEqual(analysis, MeanValueAnalysis)

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_analysis("ERROR")
