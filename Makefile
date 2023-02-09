INTERSECTS?=scripts/mosel.json
SEARCH_URL?=https://earth-search.aws.element84.com/v0

install:
	python -m pip install -r requirements.txt

dataset:
	python scripts/download_data.py -intersects $(INTERSECTS) --search-url $(SEARCH_URL)

unit_tests:
	python -m unittest discover tests/unit

local_test:
	sh scripts/local_test.sh
