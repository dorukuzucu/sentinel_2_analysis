INTERSECTS?=scripts/mosel.json
SEARCH_URL?=https://earth-search.aws.element84.com/v0

install:
	python -m pip install -r requirements.txt

dataset: install
	python scripts/download_data.py -intersects $(INTERSECTS) --search-url $(SEARCH_URL)