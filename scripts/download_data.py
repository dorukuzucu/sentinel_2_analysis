import argparse
import concurrent.futures
import json
import logging
import os
import traceback

from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, List

from satsearch import Search
from satstac import utils
from satstac.item import FILENAME_TEMPLATE, Item


BASE_URL = "https://earth-search.aws.element84.com/v0"
LOGGER = logging.getLogger("Dataset Downloader")
PROJECT_PATH = Path(__file__).parents[1]
TODAY = datetime.today().date()


def parse_arguments():
    """Parses input arguments for CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-url", type=str, help="URL to Earth Search API", default=BASE_URL)
    parser.add_argument("-intersects", type=str, required=False,
                        help="JSON data that fits GeoJSON format")
    parser.add_argument("-limit", type=int, required=False,
                        help="Threshold for number of results")
    parser.add_argument("-query", type=str, required=False,
                        help="A query string compatible with SAT API")
    parser.add_argument("--cloud-cover", type=int, default=40,
                        help="An integer for max cloud coverage")
    parser.add_argument("--log-level", type=str, default="INFO",
                        help="Use to set logging level")
    parser.add_argument("--output-dir", type=str, default="dataset",
                        help=" A path from project path where dataset will be downloaded")
    parser.add_argument("--date", type=str, default=f"{TODAY.replace(day=TODAY.day - 2)}/{TODAY}",
                        help="A date filter to limit results." +
                        "Should be either a single date or a range")
    return parser.parse_args()


def configure_logging(log_level: str) -> None:
    """Configures module logger

    Args:
        log_level (str): ONe of supported log levels: 
    """
    logging.getLogger('satsearch').propagate = False
    log_format = '%(asctime)s:%(levelname)s:%(message)s'
    logging.basicConfig(level=log_level.upper(), format=log_format)


def read_json(file_path: str) -> Dict:
    """ Reads given file path to a dictionary
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.loads(json_file.read())
    return data


def prepare_search_parameters(arguments) -> Dict[str, Any]:
    """Using given arguments, prepare a search body for STAC API.
    Prepared search body will be sent to STAC API

    Args:
        arguments: User defined parameters

    Returns:
        Dict[str, Any]: A dict which consists parameters of search body
    """
    search_parameters = {}
    if arguments.intersects:
        intersection = read_json(arguments.intersects)
        search_parameters.update({"intersects": intersection})
    if arguments.limit:
        search_parameters.update({"limit": arguments.limit})
    search_parameters.update({"datetime": arguments.date})

    LOGGER.debug("Search parameters: \n%s", json.dumps(search_parameters, indent=4))
    return search_parameters


def prepare_query_parameters(arguments) -> Dict[str, Any]:
    """Using given arguments, prepare query parameters for STAC API.
    Prepared query parameters will be sent to STAC API

    Args:
        arguments: User defined parameters

    Returns:
        Dict[str, Any]: A dict which consists parameters of query
    """
    query_parameters = {"eo:cloud_cover": {"lt": arguments.cloud_cover}}
    if arguments.query:
        query_json = json.loads(arguments.query)
        query_parameters.update(query_json)

    LOGGER.debug("Query parameters: \n%s", json.dumps(query_parameters, indent=4))
    return query_parameters


def download_item(item: Item, output_dir: str) -> None:
    """Downloads a single SAC STAC item
    This method is copied and updated from satstac.item.Item.download()

    Args:
        item (Item): SAC STAC item to be downloaded
        output_dir (str): Output directory for downloaded item data
    """
    overwrite = False
    for key in item._data['assets'].keys():
        asset = item.asset(key)
        if asset is None:
            continue

        ext = os.path.splitext(asset['href'])[1]
        filename = item.get_path(FILENAME_TEMPLATE) + '_' + key + ext
        file_path = os.path.join(PROJECT_PATH, output_dir, filename)
        if not os.path.exists(file_path) or overwrite:
            try:
                utils.download_file(asset['href'], filename=file_path,
                                    requester_pays=False, headers={})
            except Exception as exception:
                LOGGER.error("Unable to download %s: %s", asset['href'], str(exception))
                LOGGER.debug(traceback.format_exc())


def download_items(items: List[Item], output_dir: str) -> None:
    """Downloads all the STAC Items to given directory

    Args:
        items (List[Item]): Items to be downloaded
        output_dir (str): Dataset directory to download items
    """
    download_fn = partial(download_item, output_dir=output_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_fn, items)
    LOGGER.info("Download operation has been completed")



def main():
    """Main function that searches and fetches Sentinel-2 imagery 
    """
    args = parse_arguments()
    configure_logging(args.log_level)
    LOGGER.info("Configuring download operation")

    search_parameters = prepare_search_parameters(args)
    query_parameters = prepare_query_parameters(args)
    search_parameters.update({"query": query_parameters})
    LOGGER.info("Configured parameters: \n %s", json.dumps(search_parameters, indent=4))

    search = Search(url=BASE_URL, **search_parameters)
    # Access protected variable to download with Threads.
    # Default implementation only supports sequential download
    item_collection: List[Item] = search.items()._items  
    download_items(item_collection, args.output_dir)


if __name__ == "__main__":
    main()
