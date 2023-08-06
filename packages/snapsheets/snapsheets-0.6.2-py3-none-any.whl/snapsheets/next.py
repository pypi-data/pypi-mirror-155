"""Snapsheets Next

Wget Google spreadsheet

usage: snapsheets-next [-h] [--config config | --url url] [-o filename] [-d description] [-t format] [-v] [--skip]

snapsheets

Optional arguments:
    -h, --help       show this help message and exit
    --config config  set config file or directory.
    --url url        set URL of Google spreadsheet.
    -o filename      set output filename.
    -d description   set description of a spreadsheet.
    -t format        set datetime prefix for backup filename.
    -v, --version    show program's version number and exit
"""

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import pendulum
import tomli
import yaml
from icecream import ic
from loguru import logger
from snapsheets import __version__


@dataclass
class Sheet:
    """
    A class for single spreadsheet information

    Parameters
    -------
    url: str
        URL of Google spreadsheet.
    filename: str o Path
        output filename.
    description: str
        description of a sheet.
    datefmt: str
        datetime prefix for backup filename.
    skip: bool
        set to True if you want to skip.
    """

    url: str
    filename: str
    description: str
    datefmt: str = "%Y%m%d"
    skip: bool = False

    def __post_init__(self) -> None:
        o = urlparse(self.url)
        if o.netloc not in ["docs.google.com"]:
            error = f"URL should start with 'https://docs.google.com/' : {self.url}"
            logger.error(error)
            sys.exit()

        p = Path(self.filename)
        self.suffix = p.suffix
        self.fmt = self.get_fmt()

        self.key = self.get_key()
        self.gid = self.get_gid()
        self.export_url = self.get_export_url()

    def get_fmt(self) -> str:
        """Get ``FORMAT`` from given filename.

        Returns
        -------
        str
            FORMAT ("xlsx", "ods", "csv", "tsv")
        """
        ok = ["xlsx", "ods", "csv", "tsv"]
        fmt = Path(self.filename).suffix.strip(".")
        if fmt not in ok:
            error = f"{fmt} is a wrong format. Select from {ok}."
            logger.error(error)
            sys.exit()
        return fmt

    def get_key(self) -> str:
        """Get ``KEY`` from given URL.

        Returns
        -------
        str
            KEY
        """
        p = urlparse(self.url)
        key = p.path.split("/")[3]
        return key

    def get_gid(self) -> str:
        """Get ``GID`` from given URL. Set ``gid=0`` if not found.

        Returns
        -------
        str
            GID
        """
        p = urlparse(self.url)
        gid = p.fragment.split("=")[1]
        return gid

    def get_export_url(self) -> str:
        """
        Generate export URL from given arguments.

        Returns
        -------
        str
            export URL
        """
        path = f"https://docs.google.com/spreadsheets/d/{self.key}/export"
        query = f"format={self.fmt}"
        if self.gid:
            query += f"&gid={self.gid}"
        url = f"{path}?{query}"
        return url

    def download(self) -> None:
        """
        Download spreadsheet.
        Filename can be modified in config file.
        """
        cmd = ["wget", "--quiet", "-O", self.filename, self.export_url]
        cmd = [str(c) for c in cmd if c]
        if self.skip:
            info = f"Skipped downloading {self.filename}."
            logger.info(info)
        else:
            subprocess.run(cmd)
            info = f"🤖 Downloaded as {self.filename}"
            logger.success(info)

    def backup(self) -> None:
        """
        Rename downloaded file with current datetime prefix.
        Prefix can be modified in config file.
        """

        now = pendulum.now().strftime(self.datefmt)
        savef = self.filename
        p = Path(self.filename)
        fname = f"{now}_{p.name}"
        movef = Path(p.parent, fname)
        if self.skip:
            info = f"Skipped renaming {self.filename}"
            logger.info(info)
        else:
            shutil.move(savef, movef)
            info = f"🚀 Renamed to {movef}"
            logger.success(info)

    def snapshot(self) -> None:
        """Run ``download()`` & ``backup()``"""
        logger.info(f"📣 {self.description}")
        self.download()
        self.backup()


@dataclass
class Book:
    fname: str = "config.toml"

    def __post_init__(self) -> None:
        p = Path(self.fname)
        if not p.exists():
            error = "Unable to locate config file/directory."
            error += f"Perhaps you need to create a new config file/directory. : {p}"
            logger.error(error)
            sys.exit()

        self.fnames = self.get_fnames()
        self.config = self.load_config()
        self.sheets = self.get_sheets()

    def get_fnames(self) -> list[Path]:
        """
        Get list of config files.

        Returns
        -------
        list[Path]
            list of config files
        """
        p = Path(self.fname)
        logger.info(f"Load config : {p}")

        if p.is_file():
            return [p]

        fnames = sorted(p.glob("*.toml"))
        return fnames

    def load_config(self) -> dict:
        """Load configurations in TOML format.

        Returns
        -------
        dict
            configuration in dict-object
        """
        config = {}
        for fname in self.fnames:
            suffix = fname.suffix
            if suffix in [".toml"]:
                _config = self.load_config_toml(fname)
            elif suffix in [".yml", ".yaml"]:
                _config = self.load_config_yaml(fname)
            else:
                error = f"Wrong config format. '{suffix}' not supported."
                logger.error(error)
                sys.exit()
            config.update(_config)
        return config

    def load_config_toml(self, fname: Path) -> dict:
        """Load configurations from TOML format.
        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("rb") as f:
            config = tomli.load(f)
        return config

    def load_config_yaml(self, fname: Path) -> dict:
        """
        Load configurations from YAML format.

        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("r") as f:
            config = yaml.safe_load(f)
        return config

    def get_sheets(self) -> list[Sheet]:
        """
        Get list of sheets in configuration.

        Returns
        -------
        list[Sheet]
            list of Sheet objects
        """
        sheets = self.config.get("sheets")
        if sheets is None:
            return []

        sheets = []
        for sheet in self.config["sheets"]:
            url = sheet.get("url")
            filename = sheet.get("filename")
            desc = sheet.get("desc")
            datefmt = sheet.get("datefmt")
            skip = sheet.get("skip")
            _sheet = Sheet(
                url=url,
                filename=filename,
                description=desc,
                datefmt=datefmt,
                skip=skip,
            )
            sheets.append(_sheet)
        return sheets

    def snapshots(self) -> None:
        """
        Take a snapshot of sheets.
        """

        for sheet in self.sheets:
            sheet.snapshot()


def cli() -> None:
    """
    Command Line Interface for snapsheets.
    """
    ic.enable()

    parser = argparse.ArgumentParser(description="snapsheets")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--config",
        metavar="config",
        default="config.toml",
        help="set config file or directory",
    )
    group.add_argument(
        "--url",
        metavar="url",
        help="set URL of Google spreadsheet",
    )
    parser.add_argument(
        "-o",
        metavar="filename",
        default="snapshot.csv",
        help="set output filename",
    )
    parser.add_argument(
        "-d",
        metavar="description",
        default="Add description here.",
        help="set description of a spreadsheet",
    )
    parser.add_argument(
        "-t",
        metavar="format",
        default="",
        help="set datetime prefix for backup filename",
    )
    parser.add_argument("--skip", action="store_true", help="skip file")
    parser.add_argument("--debug", action="store_true", help="show more messages")
    parser.add_argument("--version", action="version", version=f"{__version__}")

    args = parser.parse_args()

    # setup logger
    logger.remove()
    if args.debug:
        fmt = "{time:YYYY-MM-DDTHH:mm:ss} | <level>{level:8}</level> | <cyan>{name}.{function}:{line}</cyan> | <level>{message}</level>"
        logger.add(sys.stderr, format=fmt, level="DEBUG")
    else:
        fmt = "{time:YYYY-MM-DDTHH:mm:ss} | <level>{level:8}</level> | <level>{message}</level>"
        logger.add(sys.stderr, format=fmt, level="SUCCESS")

    if args.url:
        sheet = Sheet(
            url=args.url,
            filename=args.o,
            description=args.d,
            datefmt=args.t,
            skip=args.skip,
        )
        sheet.snapshot()
    else:
        book = Book(args.config)
        book.snapshots()


if __name__ == "__main__":
    cli()
