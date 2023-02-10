import ctypes
import enum
import logging

from abc import ABC, abstractmethod
from multiprocessing import Manager
from typing import Any, Dict, Union

import numpy as np
from .types import RasterImage


LOGGER = logging.getLogger("Analysis")
manager = Manager()


class Analysis(ABC):
    """Base class to use for analysis on raster data
    """
    @abstractmethod
    def add(self, raster_image: RasterImage) -> None:
        """Adds a new raster image to current set
        Later, analysis will be calculated over these set

        Args:
            raster_image (RasterImage): image to analyze
        """

    @abstractmethod
    def result(self):
        """Returns result of an analysis
        """


class MeanValueAnalysis(Analysis):
    """A class to calculate mean of all pixel values within an image
    """
    pixel_count: manager.Value
    average_mean: manager.Value

    def __init__(self) -> None:
        self.pixel_count = manager.Value(ctypes.c_double, 0.0)
        self.average_mean = manager.Value(ctypes.c_double, 0.0)

    def add(self, raster_image: RasterImage) -> None:
        image_array = raster_image.array()

        image_pixel_count = np.prod(image_array.shape)
        image_sum = image_array.sum()

        self.average_mean.value = (self.average_mean.value * self.pixel_count.value + image_sum) / (self.pixel_count.value + image_pixel_count)
        self.pixel_count.value += image_pixel_count

    def result(self):
        return self.average_mean.value


class AnalysisType(enum.Enum):
    """A list of available analysis types"""
    MEAN_VALUE = "MEAN_VALUE"


_ANALYSIS_TYPE_TO_CLASS: Dict[AnalysisType, Any] = {
    AnalysisType.MEAN_VALUE: MeanValueAnalysis
}


def get_analysis(analysis_type: Union[str, AnalysisType]):
    """Retrieves analysis class based on given type

    Args:
        analysis_type (Union[str, AnalysisType]): Name or enum of analysis

    Raises:
        ValueError: If an invalid type is passed, value error is raised

    Returns:
        class: An Analysis class
    """
    if isinstance(analysis_type, str):
        try:
            analysis_type = AnalysisType[analysis_type]
        except KeyError as error:
            message = f"Invalid analysis type: {error}"
            LOGGER.error(message)
            raise ValueError(message) from error
    return _ANALYSIS_TYPE_TO_CLASS[analysis_type]
