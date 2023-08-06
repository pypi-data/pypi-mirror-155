#!/usr/bin/env python
# # xm2csv
# Script for converting xml documents into csvs where the key col is a coordinate for spatial plotting in GIS
# %% Imports
from __future__ import annotations

import argparse
import csv
import logging
import xml.etree.ElementTree as et
from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import NamedTuple
from typing import Optional

logger = logging.getLogger(__name__)

# %% parsing


def describe(elem: et.Element) -> None:
    logger.debug(f"{elem.tag=}\n{elem.attrib=}\n{elem.text=}")


def dump(elem: et.Element) -> None:
    logger.debug("Dumping {elem.tag!r}")
    for text in elem.itertext():
        logger.info(text)


# Derived from header of xml file, these are required to look tags up
# <Collections
# xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
# xmlns:dc="http://purl.org/dc/elements/1.1/"
# xmlns:dcterms="http://purl.org/dc/terms/"
# xmlns:ads="https://archaeologydataservice.ac.uk/">
# Note https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree
# explains how to generate these from the file instead of hardcoding
NAMESPACES = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ads": "https://archaeologydataservice.ac.uk/",
}


@dataclass
class SubjectPeriod:  # <dc:subjectPeriod>
    subject: str  # <dc:subject>Well</dc:subject>
    temporal: str  # <dcterms:temporal>1068 - 1300</dcterms:temporal>


MISSING_TAG_TEXT = ""  # if either of the above fields is missing, this is used


class DatatableRow(NamedTuple):
    coord_east: float
    coord_north: float
    name: str
    source: str
    primary_identifier: str
    count_of_identifiers: int
    primary_tag_subject: str
    primary_tag_temporal: str
    secondary_tag_subject: str
    secondary_tag_temporal: str
    count_of_period_tags: int


@dataclass
class ParsedLoaction:
    name: str  # <dc:title>Medieval and later well in the inner bailey of Exeter Castle</dc:title>
    source: str  # <dc:source>https://archaeologydataservice.ac.uk/archsearch/record?titleId=1816966</dc:source>
    identifiers: list[str]  # <dc:identifier>Depositor ID: 11262.0</dc:identifier>
    # <dc:identifier>ECHER11-11262.0</dc:identifier>
    coords: list[
        str
    ]  # <dcterms:spatial xsi:type="dcterms:POINT">-3.5, 50.7</dcterms:spatial>
    tags: list[SubjectPeriod]  # <dc:subjectPeriod>

    def as_datatable_rows(self) -> Generator[DatatableRow, None, None]:
        n_tags = len(self.tags)
        n_identifiers = len(self.identifiers)
        # assert n_tags >= 1, f"\n=> At {self}:\n==> Must include at least 1 temporal tag, got {n_tags}"
        assert (
            n_identifiers >= 1
        ), f"\n=> At {self}:\n==> Expect at least 1 identifier tag, got {n_identifiers}"
        for coord in self.coords:
            coord_e, coord_n = coord.split(",")
            primary_tag = (
                self.tags or [SubjectPeriod(MISSING_TAG_TEXT, MISSING_TAG_TEXT)]
            )[
                0
            ]  # in case of 0 tags
            yield DatatableRow(
                coord_east=float(coord_e),
                coord_north=float(coord_n),
                name=self.name,
                source=self.source,
                primary_identifier=self.identifiers[-1],
                count_of_identifiers=n_identifiers,
                primary_tag_subject=primary_tag.subject,
                primary_tag_temporal=primary_tag.temporal,
                secondary_tag_subject="" if n_tags < 2 else self.tags[1].subject,
                secondary_tag_temporal="" if n_tags < 2 else self.tags[1].temporal,
                count_of_period_tags=n_tags,
            )


def parse_record(record_elem: et.Element) -> ParsedLoaction:
    # assert element is of correct type
    assert (
        record_elem.attrib.get("type", None) == "record"
    ), "Parse error, record has incorrect type attribute"

    return ParsedLoaction(
        name=record_elem.findtext(
            "dc:title",
            namespaces=NAMESPACES,
            default="",
        ),
        source=record_elem.findtext(
            "dc:source",
            namespaces=NAMESPACES,
            default="",
        ),
        identifiers=[
            elem.text or ""
            for elem in record_elem.iterfind("dc:identifier", namespaces=NAMESPACES)
        ],
        coords=[
            elem.text or ""
            for elem in record_elem.iterfind("dcterms:spatial", namespaces=NAMESPACES)
            if elem.attrib  # filter out the spaticl tags with some type specifed like xsi:type="dcterms:POINT"
        ],
        tags=[
            SubjectPeriod(
                subject=elem.findtext(
                    "dc:subject",
                    namespaces=NAMESPACES,
                    default=MISSING_TAG_TEXT,
                ),
                temporal=elem.findtext(
                    "dcterms:temporal",
                    namespaces=NAMESPACES,
                    default=MISSING_TAG_TEXT,
                ),
            )
            for elem in record_elem.findall("dc:subjectPeriod", namespaces=NAMESPACES)
        ],
    )


def records_to_rows(
    records: Iterable[et.Element],
) -> Generator[DatatableRow, None, None]:
    for record in records:
        yield from parse_record(record).as_datatable_rows()


def parse_file(
    xml_in: Path,
    out_dir: Path | None = None,
    filetitle: str | None = None,
) -> Path:

    tree = et.parse(xml_in)
    root = tree.getroot()
    records = root.iter("record")
    # the first line in the xml is a title, skip this
    title_elem = next(records)
    describe(title_elem[0])
    # filetitle = title_elem.findtext("dc:title", namespaces=NAMESPACES, default="out")
    file_rows = records_to_rows(records)
    out_csv = (out_dir or xml_in.parent) / Path(filetitle or xml_in.name).with_suffix(
        ".csv",
    )
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        first_row = next(file_rows)
        writer = csv.DictWriter(f, fieldnames=first_row._fields)
        writer.writeheader()
        writer.writerow(first_row._asdict())
        # Comment out below if you just want the first line written for debugging
        logger.debug("Writing file %s", f)
        writer.writerows(map(DatatableRow._asdict, file_rows))
        logger.debug("Writing complete!")
    return out_csv


# %% main


def named_file(s: str, suffix: str) -> Path:
    try:
        p = Path(s)
    except Exception:
        raise argparse.ArgumentTypeError(f"Expected filepath but got {s!s}")

    if not p.suffix:
        return p.with_suffix(suffix)
    elif p.suffix.casefold() == suffix.casefold():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Expected {suffix} file but got {p!s}",
        )


def directory(s: str) -> Path:
    try:
        p = Path(s)
    except Exception:
        raise argparse.ArgumentTypeError(f"Expected a filepath but got {s!s}")

    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"Expected a directory got {p!s}")

    return p


def main(argv: Sequence[str] | None = None) -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "xml_file",
        type=partial(named_file, suffix=".xml"),
        help="XML file input",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        type=directory,
        help="Directory to save output to, defaults to match the input xml",
    )
    parser.add_argument(
        "-c",
        "--csv-filename",
        type=partial(named_file, suffix=".csv"),
        help="File to save output to, defaults to match the filename of the input xml",
    )

    args = parser.parse_args(argv)
    assert args.xml_file.exists(), f"'{args.xml_file.absolute()!s}' was not found"

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    result = parse_file(args.xml_file, args.output_dir, args.csv_filename)

    print(f" Wrote '{result.absolute()!s}'!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
