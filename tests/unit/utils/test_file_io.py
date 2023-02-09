import unittest
from typing import Optional
from unittest.mock import Mock, patch

from raster_analysis_service.utils.file_io import Globber


EXT_TIF = "tif"
EXT_TIF_WITH_POINT = ".tif"
TEST_START_DIR = "START_DIR"


class GlobberTestBase(unittest.TestCase):
    globber: Optional[Globber]

    def setUp(self) -> None:
        self.globber = Globber(TEST_START_DIR)

    def tearDown(self) -> None:
        self.globber = None


class GlobberAddExtensionTest(GlobberTestBase):
    def test_add_extension(self):
        self.globber.add_extension(EXT_TIF)

        self.assertListEqual(self.globber._extensions, [EXT_TIF])

    def test_add_extensions_remove_point(self):
        self.globber.add_extension(EXT_TIF_WITH_POINT)

        self.assertListEqual(self.globber._extensions, [EXT_TIF])

    def test_add_extension_does_not_duplicate(self):
        self.globber.add_extension(EXT_TIF)
        self.globber.add_extension(EXT_TIF_WITH_POINT)

        self.assertListEqual(self.globber._extensions, [EXT_TIF])

    def test_add_multiple_extensions(self):
        second_ext = EXT_TIF + "_2"
        self.globber.add_extension(EXT_TIF)
        self.globber.add_extension(second_ext)

        self.assertListEqual(self.globber._extensions, [EXT_TIF, second_ext])


class GlobberCreateTest(GlobberTestBase):
    @patch("raster_analysis_service.utils.file_io.glob")
    @patch("raster_analysis_service.utils.file_io.chain")
    def test_create_recursive_true(self, mock_chain: Mock, mock_glob: Mock):
        self.globber.add_extension(EXT_TIF)
        self.globber.create(recursive=True)

        search_string = f"{TEST_START_DIR}/**/*.{EXT_TIF}"
        mock_glob.iglob.assert_called_once_with(search_string, recursive=True)
        mock_chain.assert_called_once_with([mock_glob.iglob.return_value])

    @patch("raster_analysis_service.utils.file_io.glob")
    @patch("raster_analysis_service.utils.file_io.chain")
    def test_create_recursive_false(self, mock_chain: Mock, mock_glob: Mock):
        self.globber.add_extension(EXT_TIF)
        self.globber.create(recursive=False)

        search_string = f"{TEST_START_DIR}/*.{EXT_TIF}"
        mock_glob.iglob.assert_called_once_with(search_string, recursive=False)
        mock_chain.assert_called_once_with([mock_glob.iglob.return_value])