FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./dataset /code/dataset

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./raster_analysis_service /code/raster_analysis_service

CMD ["uvicorn", "raster_analysis_service.app:app", "--host", "0.0.0.0", "--port", "8000"]