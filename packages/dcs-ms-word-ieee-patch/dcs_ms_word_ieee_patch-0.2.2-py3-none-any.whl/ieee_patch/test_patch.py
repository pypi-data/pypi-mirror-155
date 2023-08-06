from pathlib import Path
from bs4 import BeautifulSoup
import pytest
from pytest_snapshot.plugin import Snapshot

from .patch import patch


@pytest.mark.parametrize("testname", ["test1", "test2", "test3", "test4", "test5"])
def test_happy_path_compressed(testname: str, snapshot: Snapshot):
    snapshot.snapshot_dir = Path("tests", "snapshots")
    original = Path("tests", "assets", f"{testname}.xml")

    actual = patch(
        original.read_text(encoding="utf-8"), prettify=True, compress_citation=True
    )
    actual_soup = BeautifulSoup(actual, features="xml")

    snapshot.assert_match(actual_soup.prettify(), f"{testname}-compressed-citation.xml")


@pytest.mark.parametrize("testname", ["test1", "test2", "test3", "test4", "test5"])
def test_happy_path_uncompressed(testname: str, snapshot: Snapshot):
    snapshot.snapshot_dir = Path("tests", "snapshots")
    original = Path("tests", "assets", f"{testname}.xml")

    actual = patch(
        original.read_text(encoding="utf-8"), prettify=True, compress_citation=False
    )
    actual_soup = BeautifulSoup(actual, features="xml")

    snapshot.assert_match(
        actual_soup.prettify(), f"{testname}-uncompressed-citation.xml"
    )
