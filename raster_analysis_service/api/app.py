import logging
import os
from fastapi import FastAPI
from .analyze_service import AnalyzeService
from .types import AnalysisRequest


def configure_logging(log_level: str) -> None:
    """Configures module logger

    Args:
        log_level (str): ONe of supported log levels: 
    """
    logging.getLogger('rasterio').propagate = False

    log_format = '%(asctime)s:%(levelname)s:%(message)s'
    logging.basicConfig(level=log_level.upper(), format=log_format)


configure_logging(os.environ.get("LOG_LEVEL", "DEBUG"))
LOGGER = logging.getLogger("Service")
app = FastAPI()



@app.post("/analyze")
async def dataset_mean_value(request: AnalysisRequest):
    """Calculate mean value for images"""
    service = AnalyzeService()
    result = service.analyze(request.name)
    return result


@app.get("/operations")
async def supported_operations():
    """List Supported Operations"""
    service = AnalyzeService()
    return service.supported_operations()
