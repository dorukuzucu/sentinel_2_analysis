from typing import Any
import numpy as np
import rasterio


class RasterImage:
    raster_image_path: str
    raster_data: Any

    def __init__(self, raster_image_path: str) -> None:
        self.raster_image_path = raster_image_path
        self.raster_data = rasterio.open(raster_image_path)

    def array(self) -> np.ndarray:
        """Retrieves numpy array of opened dataset item

        Returns:
            np.ndarray: raster values of selected item
        """
        images = []
        for idx in self.raster_data.indexes:
            images.append(self.raster_data.read(idx))
        return np.array(images)
