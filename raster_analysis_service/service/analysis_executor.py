import concurrent.futures
import logging

from abc import ABC, abstractmethod
from typing import Iterable

from raster_analysis_service.image.analysis import Analysis
from raster_analysis_service.image.types import RasterImage
from raster_analysis_service.utils.constants import ANALYSIS_WORKERS


LOGGER = logging.getLogger("Analysis")


class ExecutorBase(ABC):
    _analysis: Analysis
    _dataset: Iterable

    def __init__(self, analysis: Analysis, dataset: Iterable) -> None:
        self._analysis = analysis
        self._dataset = dataset

    @abstractmethod
    def execute(self):
        """Execute analysis on given dataset"""

    def _analyze_image(self, image_path: str):
        LOGGER.debug("Processing image at %s", str(image_path))
        raster_image = RasterImage(image_path)
        self._analysis.add(raster_image)


class SequentialExecutor(ExecutorBase):
    """Executes an analysis on a dataset sequentially"""
    def execute(self):
        for image_path in self._dataset:
            self._analyze_image(image_path)


class ProcessBasedExecutor(ExecutorBase):
    """Executes an analysis on a dataset using Process based paralellism"""
    _workers: int

    def __init__(self, analysis: Analysis, dataset: Iterable, num_workers: int = ANALYSIS_WORKERS) -> None:
        super().__init__(analysis, dataset)
        self._workers = num_workers

    def execute(self):
        with concurrent.futures.ProcessPoolExecutor(self._workers) as executor:
            executor.map(self._analyze_image, self._dataset)


def get_executor_type() -> ExecutorBase:
    """Return executor type based on number of processes provided"""
    if ANALYSIS_WORKERS > 1:
        return ProcessBasedExecutor
    else:
        return SequentialExecutor
