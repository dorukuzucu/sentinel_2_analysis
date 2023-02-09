INTERSECTS?=scripts/mosel.json
SEARCH_URL?=https://earth-search.aws.element84.com/v0

DOCKER_IMAGE_NAME?=raster_analysis_service

install:
	python -m pip install -r requirements.txt

dataset:
	python scripts/download_data.py -intersects $(INTERSECTS) --search-url $(SEARCH_URL)

unit_tests:
	python -m unittest discover tests/unit

local_run:
	 uvicorn raster_analysis_service.app:app --host 0.0.0.0 --port 8000

api_test:
	sh scripts/local_test.sh

docker:
	docker build --tag $(DOCKER_IMAGE_NAME) .

docker_run:
	docker run -p8000:8000 $(DOCKER_IMAGE_NAME) 
