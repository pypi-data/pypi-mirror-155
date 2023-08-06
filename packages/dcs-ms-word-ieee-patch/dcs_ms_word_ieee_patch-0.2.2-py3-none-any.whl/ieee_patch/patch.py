from pathlib import Path
from typing import Any, List
import typer
from bs4 import BeautifulSoup
import xml.dom.minidom
from operator import itemgetter
from itertools import groupby
import copy
import zipfile
import sys
import logging
import shutil
import re
import os
import tempfile

app = typer.Typer()

# logging.captureWarnings(True)
logger = logging.Logger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main():
    app()


@app.command(
    help=(
        "Patch IEEE citation reference format in Microsoft Word docx "
        "documents.\n\n"
        "The tool converts citations in the form '[1], [2], [3], [5]' to the "
        "IEEE compliant citation format [1]-[3],[5] or optional to the "
        "compressed form [1-3,5].\n"
        "An optional comma combined with spaces as separators between the "
        "citations in the original file are understood and respected by the "
        "script.\n\n"
        "IEEE citation format is described in this document: "
        "https://ieeeauthorcenter.ieee.org/wp-content/uploads/IEEE-Reference-Guide.pdf"
    )
)
def run(
    docx_file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="Path to docx file that should be fixed.",
    ),
    overwrite: bool = typer.Option(
        False,
        help=(
            "Overwrites the file instead of creating a copy and working on the copy."
        ),
    ),
    compress_citation: bool = typer.Option(
        False,
        help="Compress citation references, e.g. '[1], [2], [3], [5]' becomes '[1-3,5]'.",
    ),
):
    try:
        if overwrite:
            new_docx_file = docx_file
        else:
            new_docx_file = _patch_filename(docx_file)
            shutil.copy(docx_file, new_docx_file)

        xml_document_path = Path("word", "document.xml").as_posix()

        with zipfile.ZipFile(new_docx_file, "a") as archive:
            # The xml file that need to be patched is located in
            # `word/document.xml` and does contain all relevant content for the
            # whole document.
            with archive.open(xml_document_path, "r") as fh:
                doc = fh.read().decode("utf-8")

        patched_doc = patch(doc, compress_citation=compress_citation)

        _update_single_file_in_zip(new_docx_file, xml_document_path, patched_doc)

        sys.exit(0)

    except zipfile.BadZipFile as error:
        logger.error(error)
        sys.exit(1)


def _patch_filename(fp: Path):
    parts = list(fp.parts)
    fn = parts[-1].split(".")
    fn.insert(len(fn) - 1, "patched")
    parts[-1] = ".".join(fn)
    return Path(*parts)


def _update_single_file_in_zip(zipname: os.PathLike, filename: str, data: str):
    """
    Updates a single file in a zip archive, which is something the zipfile lib
    from the stdlib cannot handle.

    Author: sebdelsol (https://stackoverflow.com/users/3692322/sebdelsol)
    Source: https://stackoverflow.com/a/25739108/434227
    License: CC BY-SA 3.0
    """
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename
    with zipfile.ZipFile(zipname, "r") as zin:
        with zipfile.ZipFile(tmpname, "w") as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)


def _create_simple_text_tag(soup: BeautifulSoup, char: str):
    tag = soup.new_tag("w:r", attrs={"w:rsidR": "007022E7"})
    tag2 = soup.new_tag("w:t")
    tag2.string = char
    tag.append(tag2)
    return tag


def rewrite_simple(bag: List[Any], strip: List[Any]):
    for i in range(1, len(bag) - 1):
        bag[i].extract()
    for el in strip:
        el.extract()


def get_cite_id(el) -> int:
    regex = re.compile(r"^\[?(\d+)")
    for tn in el.find_all("w:t"):
        if tn.text.strip() == "":
            continue

        # we found a match, see if we should keep it
        matches = regex.match(tn.text)
        cite_digit = 0
        if matches is not None and len(matches.groups()) == 1:
            cite_digit: int = int(matches.group(1))
        else:
            logger.error(f"No citation identifier found for string '{tn.text}'")
        return cite_digit

    return 0  # this case should never happen


def _strip_space_remove_brackets(el, compress_citation: bool = False):
    text_nodes = el.find_all("w:t")
    for tn in text_nodes:
        # strip space-only nodes
        if tn.text.strip() == "":
            tn.parent.extract()  # remove any protected spaces
            continue

        # remove brackets
        tn.string = tn.text.strip()
        if compress_citation:
            tn.string = tn.string[1:-1]


def rewrite_complex(
    soup: BeautifulSoup,
    bag: List[Any],
    strip: List[Any],
    compress_citation: bool = False,
):
    # first remove all separating chars
    for el in strip:
        el.extract()

    for el in bag:
        _strip_space_remove_brackets(el, compress_citation=compress_citation)

    # 1. sort citations
    sbag = sorted(bag, key=lambda el: get_cite_id(el))
    sbag = [copy.copy(el) for el in sbag]  # deep copy for later rewrite
    ids = [get_cite_id(el) for el in sbag]

    # create hashmap
    sbag_map = {}
    for i, id_ in enumerate(ids):
        sbag_map[id_] = sbag[i]

    for i, el in enumerate(bag):  # change order of existing ones
        el.replace_with(sbag[i])

    # 2. remove duplicates
    seen = []
    for i, id_ in enumerate(ids[::-1]):
        if id_ not in seen:
            seen.append(id_)
            continue
        sbag.pop(i)
        ids.pop(i)
    del seen

    groups = []
    groups_iter = groupby(enumerate(ids), lambda x: x[0] - x[1])
    for _, g in groups_iter:
        groups.append(list(g))

    for i, g in enumerate(groups):
        group = map(itemgetter(1), g)
        group = list(map(int, group))
        if len(group) == 2:
            sbag_map[group[0]].insert_after(_create_simple_text_tag(soup, ","))
        if len(group) <= 2 and i != len(groups) - 1:
            sbag_map[group[-1]].insert_after(_create_simple_text_tag(soup, ","))
            continue
        for j, jx in enumerate(group):
            if j == 0:
                continue
            elif j == len(group) - 1:
                continue
            elif j == 1:
                # replace first middle element
                sbag_map[jx].replace_with(_create_simple_text_tag(soup, "-"))
            else:
                # remove all other middle elements
                sbag_map[jx].extract()

    if compress_citation:
        sbag[0].insert_before(_create_simple_text_tag(soup, "["))
        sbag[-1].insert_after(_create_simple_text_tag(soup, "]"))


def patch(content: str, prettify: bool = False, compress_citation: bool = False) -> str:
    soup = BeautifulSoup(content, features="xml")
    paragraphs = soup.find_all("w:p")

    bags = []
    strips = []
    for p in paragraphs:
        bag = []
        strip = []
        for child in p.children:
            # Remove any newline characters.
            if child.text == "\n":
                strip.append(child)
            # citations have the tag `w:sdt` and have a children `<w:citation/>`
            elif child.name == "sdt" and child.find("w:citation") is not None:
                bag.append(child)
            # If we have at least one element in the bag and the striped text
            # boils down to only a comma or no text at all, we are in between
            # two citations. Any stuff in between the citations should go to the
            # strip array.
            elif len(bag) > 0 and child.name == "r" and child.text.strip() in [",", ""]:
                strip.append(child)
            else:
                # register block (bag + strips)
                if len(bag) > 0:
                    bags.append(bag)
                    strips.append(strip)
                bag = []
                strip = []

        # register block if anything has been found which has not been registred yet
        if len(bag) > 0:
            if len(bag) > 0:
                bags.append(bag)
                strips.append(strip)
            bag = []
            strip = []

    for bag, strip in zip(bags, strips):
        rewrite_complex(soup, bag, strip, compress_citation=compress_citation)

    xml_content = str(soup).replace("\n", "")
    if prettify:
        return xml.dom.minidom.parseString(xml_content).toprettyxml()
    else:
        return xml_content


if __name__ == "__main__":
    app()
