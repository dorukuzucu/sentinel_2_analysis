import logging
from typing import Iterable
from raster_analysis_service.image.analysis import Analysis, AnalysisType, get_analysis
from raster_analysis_service.image.types import RasterImage
from raster_analysis_service.utils.constants import ABSOLUTE_DATASET_PATH
from raster_analysis_service.utils.file_io import Globber


LOGGER = logging.getLogger("Analysis")


def create_tif_dataset():
    dataset_globber: Globber = Globber(ABSOLUTE_DATASET_PATH)
    # dataset_globber.add_includes("overview")
    dataset_globber.add_extension("tif")
    return dataset_globber.create(recursive=True)


class AnalyzeService:
    analysis: Analysis

    def __init__(self) -> None:
        self.analysis = None

    def supported_operations(self):
        """A functions to retrieve supported analysis types"""
        operations = [analysis.value for analysis in AnalysisType]
        LOGGER.debug("Operations %s", str(operations))
        return operations

    def analyze(self, analysis_name: str):
        self.analysis: Analysis = get_analysis(analysis_name)()
        dataset = create_tif_dataset()

        self._analyze_dataset(dataset)
        return self.analysis.result()

    def _analyze_dataset(self, dataset: Iterable):
        for image_path in dataset:
            self._analyze_image(image_path)

    def _analyze_image(self, image_path: str):
        LOGGER.debug("Processing image at %s", str(image_path))
        raster_image = RasterImage(image_path)
        self.analysis.add(raster_image)
