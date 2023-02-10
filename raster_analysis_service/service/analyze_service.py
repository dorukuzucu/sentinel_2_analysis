import logging

from raster_analysis_service.image.analysis import Analysis, AnalysisType, get_analysis
from raster_analysis_service.service.analysis_executor import ExecutorBase, get_executor_type
from raster_analysis_service.utils.constants import ABSOLUTE_DATASET_PATH
from raster_analysis_service.utils.file_io import Globber


LOGGER = logging.getLogger("Analysis")


def create_tif_dataset():
    LOGGER.info("Preparing available images list")
    dataset_globber: Globber = Globber(ABSOLUTE_DATASET_PATH)
    # dataset_globber.add_includes("overview")
    dataset_globber.add_extension("tif")
    return dataset_globber.create(recursive=True)


class AnalyzeService:
    def supported_operations(self):
        """A functions to retrieve supported analysis types"""
        LOGGER.info("Retrieving supported operations")
        operations = [analysis.value for analysis in AnalysisType]
        LOGGER.debug("Operations %s", str(operations))
        return operations

    def analyze(self, analysis_name: str):
        """Perform given analyze on downloaded data"""
        LOGGER.debug("Making preparation to calculate %s", analysis_name)
        analysis: Analysis = get_analysis(analysis_name)()
        dataset = create_tif_dataset()

        LOGGER.info("Starting calculations for %s", analysis_name)
        executor: ExecutorBase = get_executor_type()(analysis, dataset)
        executor.execute()
        LOGGER.info("Calculation has been completed")
        return analysis.result()
