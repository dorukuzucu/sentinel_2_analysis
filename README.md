# **Sentinel 2 Analysis**
A simple API in Python to search a Sentinel-2 satellite scene and compute the mean value of the raster imagery values

## **Usage**

### **Installing requirements to currently active environment**

```shell
make install
```

### **Downloading the dataset**

#### **Via Makefile**

```shell
make dataset
```

Following parameters can be passed to make command:
- INTERSECTS: A path to Coordinates in Geojson format. Results intersecting with given coordinates will be searched and fetched(default is scripts/mosel.json)
- SEARCH_URL: Use this to change data search url(default is https://earth-search.aws.element84.com/v0)

Another way to download dataset is to call download script directly. This method enables user and gives access to more parameters

#### **Via Python Script**

```shell
python scripts/download_data.py
```
Following parameters can be passed to python script:

| Parameter | Explanation | Default |
|-----------|-------------|---------|
| --search-url | URL to Earth Search API | https://earth-search.aws.element84.com/v0 |
| -intersects | JSON data that fits GeoJSON format | None |
| -limit | Threshold for number of results | None |
| -query | A query string compatible with SAT API | cloud_cover<40 |
| --cloud-cover | An integer for max cloud coverage | 40 |
| --log-level | Use to set logging level | INFO |
| --output-dir | A path from project path where dataset will be downloaded | dataset |
| --date | A date filter to limit results. Should be either a single date or a range | (TODAY - 2 DAYS)/TODAY
