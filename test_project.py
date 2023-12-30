from project import (
    checkFileExist,
    handleFileFolderCreation,
    range_for_int,
    range_for_float,
)
import pytest
import argparse


def test_checkFileExist():
    checkFileExist("") == ""
    checkFileExist("cat.jpg") == "cat.jpg"
    checkFileExist("cat2.jpg  ") == "cat.jpg"


def test_handleFileFolderCreation():
    with pytest.raises(SystemExit):
        handleFileFolderCreation("")
        handleFileFolderCreation("cat.jpgg")

    handleFileFolderCreation("cat.mp4") == ("cat.mp4", ".mp4")


def test_range_for_int():
    with pytest.raises(argparse.ArgumentTypeError):
        range_for_int("color", 0, 2)(3)
        range_for_int("color", 0, 2)("1.2")

    range_for_int("color", 0, 2)(1) == 1
    range_for_int("color", 0, 2)(1.4) == 1


def test_range_for_float():
    with pytest.raises(argparse.ArgumentTypeError):
        range_for_float("color", 0, 2)(3)
        range_for_float("color", 0, 2)("1.2")

    range_for_float("color", 0, 2)(1.3) == 1.3
