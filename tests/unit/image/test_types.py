from typing import Optional
import unittest
from unittest.mock import call, patch

import numpy as np

from raster_analysis_service.image.types import RasterImage


TEST_IMAGE_PATH = "test_path"


class RasterImageTest(unittest.TestCase):
    raster_image: Optional[RasterImage]

    def setUp(self) -> None:
        self.patcher = patch("raster_analysis_service.image.types.rasterio")
        self.mock_rasterio = self.patcher.start()
        self.raster_image = RasterImage(TEST_IMAGE_PATH)

    def tearDown(self) -> None:
        self.raster_image = None

    def test_init_loads_data(self):
        RasterImage(TEST_IMAGE_PATH)

        self.mock_rasterio.open.assert_called_with(TEST_IMAGE_PATH)
        self.assertEqual(self.raster_image.raster_image_path, TEST_IMAGE_PATH)

    def test_array_calls_read(self):
        size = 5
        indexes = (1,)
        self.raster_image.raster_data.indexes = indexes
        self.raster_image.raster_data.read.return_value = np.zeros((size, size))
        np_array = self.raster_image.array()

        self.assertTupleEqual((len(indexes), size, size), np_array.shape)
        
        for idx in indexes:
            self.assertTrue(call(idx) in self.raster_image.raster_data.read.call_args_list)

    def test_array_calls_read_multichannel(self):
        size = 5
        indexes = (1, 2, 3)

        self.raster_image.raster_data.indexes = indexes
        self.raster_image.raster_data.read.return_value = np.zeros((size, size))
        np_array = self.raster_image.array()

        self.assertTupleEqual((len(indexes), size, size), np_array.shape)
        
        for idx in indexes:
            self.assertTrue(call(idx) in self.raster_image.raster_data.read.call_args_list)
