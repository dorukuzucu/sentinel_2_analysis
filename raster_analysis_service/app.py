import functools
import logging
import os
from fastapi import FastAPI, HTTPException
from .service.analyze_service import AnalyzeService
from .service.types import AnalysisRequest


def configure_logging(log_level: str) -> None:
    """Configures module logger

    Args:
        log_level (str): One of supported log levels
    """
    logging.getLogger('rasterio').propagate = False

    log_format = '%(asctime)s:%(levelname)s:%(message)s'
    logging.basicConfig(level=log_level.upper(), format=log_format)


configure_logging(os.environ.get("LOG_LEVEL", "DEBUG"))
LOGGER = logging.getLogger("Service")
app = FastAPI()


def with_general_exception_handling(func):
    """To handle unexpected exceptions during a request execution"""
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as exception:
            LOGGER.exception(exception)
            raise HTTPException(status_code=500, detail="An unknown error has occured.")
    return wrapped


@app.post("/analyze")
@with_general_exception_handling
async def dataset_mean_value(request: AnalysisRequest):
    """Calculate mean value for images"""
    LOGGER.info("Received Request: %s", request)
    service = AnalyzeService()
    result = service.analyze(request.name)
    LOGGER.info("Response: {%.2f}", result)
    return result


@app.get("/operations")
@with_general_exception_handling
async def supported_operations():
    """List Supported Operations"""
    service = AnalyzeService()
    return service.supported_operations()
