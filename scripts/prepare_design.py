#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

"""
This script aims to prepare the list of files to be processed
by the bam-msisensor pipeline

It iterates over a given directory, lists all bam files.

The written file is a TSV file.

You can test this script with:
pytest -v ./prepare_design.py

Usage example:
# Indexed bams example:
python3.7 ./prepare_design.py path/to/normal path/to/tumor --index

# Non-indexed bam example:
python3.7 ./prepare_design.py path/to/normal path/to/tumor

# Search in sub-directories:
python3.7 ./prepare_design.py path/to/normal path/to/tumor --index --recursive
"""

import argparse           # Parse command line
import logging            # Traces and loggings
import logging.handlers   # Logging behaviour
import os                 # OS related activities
import pandas as pd       # Parse TSV files
import pytest             # Unit testing
import shlex              # Lexical analysis
import sys                # System related methods

from pathlib import Path                        # Paths related methods
from typing import Any, Dict, Generator, List, Optional, Union   # Type hints
from os.path import commonprefix

from common import *

logger = setup_logging(logger="prepare_design.py")


# Processing functions
# Looking for fastq files
def search_bam(bam_dir: Path,
               recursive: bool = False,
               index: bool = False) -> Generator[str, str, None]:
    """
    Iterate over a directory and search for fastq files

    Parameters:
        bam_dir     Path        Path to the bam directory in which to search
        recursive   bool        A boolean, weather to search recursively in
                                sub-directories (True) or not (False)
        index       bool        Search for indexes and not for bam themselves

    Return:
                    Generator[str, str, None]       A Generator of paths

    Example:
    >>> search_bam(Path("tests/bams/"))
    <generator object search_fq at 0xXXXXXXXXXXXX>

    >>> list(search_bam(Path("tests/", True)))
    [PosixPath('tests/bam/A_R2.bam'),
     PosixPath('tests/bam/B_R2.bam')]
    """
    ext = (".bai" if index else ".bam")
    for path in bam_dir.iterdir():
        if path.is_dir():
            if recursive is True:
                yield from search_bam(path, recursive, index)
            else:
                continue

        if path.name.endswith(ext):
            yield path


# Testing search_bam
def test_search_bam():
    """
    This function tests the ability of the function "search_bam" to find the
    fastq files in the given directory

    Example:
    pytest -v prepare_design.py -k test_search_bam
    """
    path = Path("tests/")
    expected = [
        path / "normal_data" / "example.normal.bam",
        path / "tumor_data" / "example.tumor.bam"
    ]
    got = list(search_bam(path, recursive=True))
    assert sorted(got) == sorted(expected)


def test_search_bai():
    """
    This function tests the ability of the function "search_bam" to find the
    fastq files in the given directory

    Example:
    pytest -v prepare_design.py -k test_search_bam
    """
    path = Path("tests")
    expected = [
        path / "normal_data" / "example.normal.bam.bai",
        path / "tumor_data" / "example.tumor.bam.bai"
    ]
    got = list(search_bam(path, recursive=True, index=True))
    assert sorted(got) == sorted(expected)


# Turning the FQ lists into a dictionnary
def classify_bam(normal_bam_files: List[Path],
                 tumor_bam_files: List[str],
                 normal_index_files: Optional[List[Path]] = None,
                 tumor_index_files: Optional[List[Path]] = None) \
                 -> Dict[str, Path]:
    """
    Return a dictionary with identified fastq files (paried or not)

    Parameters:
        normal_bam_files    List[Path]   List of path to normal mapping files
        tumor_bam_files     List[str]    List of path to tumor mapping files
        normal_index_files  List[Path]   List of path to normal indexes files
        tumor_index_files   List[Path]   List of path to tumor indexes files

    Return:
        Dict[str, Path] A dictionary: for each Sample ID, the ID
                        is repeated alongside with the upstream
                        /downstream fastq files.

    Example:
    Incomming
    """
    bam_dict = {}
    tumor_normal_pairs = len(tumor_bam_files) == len(normal_bam_files)
    try:
        tumor_indexes = len(tumor_bam_files) == len(tumor_index_files)
        normal_indexes = len(normal_bam_files) == len(normal_index_files)
    except TypeError:
        tumor_indexes = normal_indexes = False

    if not tumor_normal_pairs:
        raise ValueError("Un-matching number of tumors/normal files")

    if tumor_indexes and normal_indexes:
        logger.debug("Bam and indexes are used in this pipeline")
        files_iterator = zip(
            normal_bam_files,
            tumor_bam_files,
            normal_index_files,
            tumor_index_files
        )

        return {
            commonprefix([nbam.name, tbam.name]): {
                "Sample_id": commonprefix([nbam.name, tbam.name]),
                "Normal_Bam": nbam,
                "Normal_Index": nbai,
                "Tumor_Bam": tbam,
                "Tumor_Index": tbai
            }
            for nbam, tbam, nbai, tbai in files_iterator
        }

    logger.debug("No bam indexes taken into account")
    return {
        commonprefix([normal.name, tumor.name]): {
            "Sample_id": commonprefix([normal.name, tumor.name]),
            "Normal_Bam": normal,
            "Tumor_Bam": tumor
        }
        for normal, tumor in zip(normal_bam_files, tumor_bam_files)
    }


def test_classify_bam_and_bai():
    """
    This function tests the classify_bam function

    Example:
    pytest -v ./prepare_design.py -k test_classify_bam
    """
    prefix = Path(__file__).parent.parent / "tests"
    expected = {
        'example.': {
            'Sample_id': 'example.',
            'Normal_Bam': prefix / "normal_data" / "example.normal.bam",
            'Bam_Index': prefix / "normal_data" / 'example.normal.bam.bai',
            'Tumor_Bam': prefix / "tumor_data" / "example.tumor.bam",
            'Bam_Index': prefix / "tumor_data" / 'example.tumor.bam.bai'
        }
    }
    logger = logging.getLogger("prepare_design.py")
    nbam = list(search_bam(prefix / "normal_data"))
    nbai = list(search_bam(prefix / "normal_data", index=True))
    tbam = list(search_bam(prefix / "tumor_data"))
    tbai = list(search_bam(prefix / "tumor_data", index=True))
    assert sorted(classify_bam(nbam, tbam, nbai, tbai)) == sorted(expected)


def test_classify_bam_only():
    """
    This function tests the classify_bam function

    Example:
    pytest -v ./prepare_design.py -k test_classify_bam
    """
    prefix = Path(__file__).parent.parent / "tests"
    expected = {
        'example.': {
            'Sample_id': 'example.',
            'Normal_Bam': prefix / "normal_data" / "example.normal.bam",
            "Tumor_Bam": prefix / "tumor_data" / "example.tumor.bam"
        }
    }
    logger = logging.getLogger("prepare_design.py")
    nbam = list(search_bam(prefix / "normal_data"))
    tbam = list(search_bam(prefix / "tumor_data"))
    assert sorted(classify_bam(nbam, tbam)) == sorted(expected)


# Parsing command line arguments
# This function won't be tested
def parse_args(args: Any = sys.argv[1:]) -> argparse.ArgumentParser:
    """
    Build a command line parser object

    Parameters:
        args    Any                 Command line arguments

    Return:
                ArgumentParser      Parsed command line object

    Example:
    >>> parse_args(shlex.split("/path/to/fasta --single"))
    Namespace(debug=False, output='design.tsv', path='/path/to/fasta',
    quiet=False, recursive=False, single=True)
    """
    # Defining command line options
    main_parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter,
        epilog="This script does not perform any magic. Check the result."
    )

    # Required arguments
    main_parser.add_argument(
        "normal_bam",
        help="Path to the directory containing normal bam files",
        type=str
    )

    main_parser.add_argument(
        "tumor_bam",
        help="Path to the directory containing tumor bam files",
        type=str
    )

    # Optional arguments
    main_parser.add_argument(
        "-r", "--recursive",
        help="Recursively search in sub-directories for fastq files",
        action="store_true"
    )

    main_parser.add_argument(
        "-i", "--index",
        help="Also search for bam indexes",
        action="store_true"
    )

    main_parser.add_argument(
        "-o", "--output",
        help="Path to output file (default: %(default)s)",
        type=str,
        default="design.tsv"
    )

    # Logging options
    log = main_parser.add_mutually_exclusive_group()
    log.add_argument(
        "-d", "--debug",
        help="Set logging in debug mode",
        default=False,
        action='store_true'
    )

    log.add_argument(
        "-q", "--quiet",
        help="Turn off logging behaviour",
        default=False,
        action='store_true'
    )

    # Parsing command lines
    return main_parser.parse_args(args)


def test_parse_args() -> None:
    """
    This function tests the command line parsing

    Example:
    >>> pytest -v prepare_config.py -k test_parse_args
    """
    options = parse_args(
        shlex.split("/path/to/normal/bam/ /path/to/tumor/bam/")
    )

    expected = argparse.Namespace(
        debug=False,
        output='design.tsv',
        normal_bam='/path/to/normal/bam/',
        tumor_bam='/path/to/tumor/bam/',
        quiet=False,
        recursive=False,
        index=False
    )

    assert options == expected


# Main function, the core of this script
def main(args: argparse.ArgumentParser) -> None:
    """
    This function performs the whole preparation sequence

    Parameters:
        args    ArgumentParser      The parsed command line

    Example:
    >>> main(parse_args(shlex.split("/path/to/bam/dir/")))
    """
    # Searching for bam files and sorting them alphabetically
    nbam = sorted(list(search_bam(Path(args.normal_bam), recursive=args.recursive)))
    tbam = sorted(list(search_bam(Path(args.tumor_bam), recursive=args.recursive)))

    logger.debug("Head of alphabetically sorted list of bam files:")
    logger.debug([str(i) for i in nbam[0:5]])
    logger.debug([str(i) for i in tbam[0:5]])

    nbai = None
    tbai = None
    if args.index is True:
        nbai = sorted(list(search_bam(Path(args.normal_bam), recursive=args.recursive, index=args.index)))
        tbai = sorted(list(search_bam(Path(args.tumor_bam), recursive=args.recursive, index=args.index)))

        logger.debug("Head of alphabetically sorted bai files:")
        logger.debug([str(i) for i in nbai[0:5]])
        logger.debug([str(i) for i in tbai[0:5]])

    # Building a dictionnary of bam with indexes
    bam_dict = classify_bam(nbam, tbam, nbai, tbai)

    # Using Pandas to handle TSV output (yes pretty harsh I know)
    data = pd.DataFrame(bam_dict).T
    logger.debug("\n{}".format(data.head()))
    logger.debug("Saving results to {}".format(args.output))
    data.to_csv(args.output, sep="\t", index=False)


# Running programm if not imported
if __name__ == '__main__':
    # Parsing command line
    args = parse_args()
    logger = setup_logging(logger="prepare_design.py", args=args)

    try:
        logger.debug("Preparing design")
        main(args)
    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)
