import concurrent.futures
import logging

from typing import Iterable

from raster_analysis_service.image.analysis import Analysis, AnalysisType, get_analysis
from raster_analysis_service.image.types import RasterImage
from raster_analysis_service.service.analysis_executor import ExecutorBase, get_executor_type
from raster_analysis_service.utils.constants import ABSOLUTE_DATASET_PATH
from raster_analysis_service.utils.file_io import Globber


LOGGER = logging.getLogger("Analysis")


def create_tif_dataset():
    dataset_globber: Globber = Globber(ABSOLUTE_DATASET_PATH)
    # dataset_globber.add_includes("overview")
    dataset_globber.add_extension("tif")
    return dataset_globber.create(recursive=True)


class AnalyzeService:
    def supported_operations(self):
        """A functions to retrieve supported analysis types"""
        operations = [analysis.value for analysis in AnalysisType]
        LOGGER.debug("Operations %s", str(operations))
        return operations

    def analyze(self, analysis_name: str):
        """Perform given analyze on downloaded data"""
        analysis: Analysis = get_analysis(analysis_name)()
        dataset = create_tif_dataset()

        executor = get_executor_type()(analysis, dataset)
        executor.execute()
        return analysis.result()
