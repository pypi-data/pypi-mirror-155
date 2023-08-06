#!/usr/bin/env python3
"""
Command-line interface to :class:`~excentis.xra31.analysis.Analysis`.
"""

# pylint: disable=logging-format-interpolation
# pylint: disable=logging-not-lazy

import argparse
import logging
import os
import pathlib
import sys

from .. import connect, exceptions, tracer, version

# Arguments
parser = argparse.ArgumentParser(
    description="Access XRA-31 capture files.  "
    "The commands can be combined, and files won't be deleted unless "
    "downloading succeeds.")

parser.add_argument("address",
                    metavar="XRA-31",
                    help="XRA-31 hostname or IP address",
                    nargs="?")
parser.add_argument("-p",
                    "--path",
                    metavar="directory/remote.pcap",
                    help="captured file on the XRA-31.  "
                    "If missing, the latest capture is downloaded.  "
                    "If --wait-end or --wait-file-end is used, "
                    "this option will be ignored.",
                    type=pathlib.PurePosixPath)
parser.add_argument("--filename", action="store_true", help=argparse.SUPPRESS)
parser.add_argument("-q",
                    "--quiet",
                    action="store_true",
                    help="don't print progress messages")
parser.add_argument("-v",
                    "--verbose",
                    action="count",
                    help="print debugging messages")
parser.add_argument("--version",
                    action="store_true",
                    help="print client version and server version")

parser_commands = parser.add_argument_group("commands")
parser_commands.add_argument("--wait-end",
                             action="store_true",
                             help="wait for the capture to end")
parser_commands.add_argument("--wait-file-end",
                             action="store_true",
                             help="wait for the next file rollover"
                             " in a rolling file capture")
parser_commands.add_argument("--download",
                             action="store_true",
                             help="store captures locally")
parser_commands.add_argument("--delete",
                             action="store_true",
                             help="remove captures from the XRA-31")
parser_options = parser.add_argument_group("command options")
parser_options.add_argument("-o",
                            "--output",
                            metavar="local.pcap",
                            help="local download location",
                            type=str)
parser_options.add_argument("-r",
                            "--rolling",
                            action="store_true",
                            help="treat path as a full rolling file capture")
parser_options.add_argument(
    "-a",
    "--append",
    action="store_true",
    help="append capture to an existing file; requires download")
parser_options.add_argument("-t",
                            "--timeout",
                            help="maximum time to wait for the end of the"
                            " capture or the rollover of a file (seconds)",
                            type=float)
parser_options.add_argument("-c",
                            "--compress",
                            action="store_true",
                            help="compress the downloaded capture file (gzip)")


def main():
    args = parser.parse_args()

    if not args.address:
        if args.version:
            print("XRA-31 client version " + version())
            sys.exit(0)
        else:
            parser.print_usage()
            print("Error: the following arguments are required: XRA-31")
            sys.exit(1)

    # Logging
    logger = logging.getLogger(pathlib.Path(sys.argv[0]).name)
    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
    if args.verbose:
        logging.root.setLevel(logging.DEBUG)
        if args.verbose > 1:
            tracer.setLevel(logging.DEBUG)
        else:
            tracer.setLevel(logging.WARNING)
    elif not args.quiet:
        logger.setLevel(logging.INFO)

    # Deprecate filename option
    if args.filename:
        logger.error("Filename has been deprecated in v5.0.0; "
                     "please use --path instead.")
        sys.exit(1)

    # Connect
    try:
        client = connect(address=args.address)
    except exceptions.Xra31VersionException as error:
        logger.error("Could not connect to an XRA-31 at \"{}\": {}.".format(
            args.address, str(error)))
        sys.exit(1)
    except exceptions.Xra31Exception as error:
        logger.error("Could not connect to an XRA-31 at \"{}\"."
                     " Please verify the host.{}{}: {}".format(
                         args.address, os.linesep,
                         type(error).__name__, str(error)))
        sys.exit(1)

    logger.info("Connected to " + str(client))

    if args.verbose:
        client.logger.setLevel(logging.DEBUG)
    elif not args.quiet:
        client.logger.setLevel(logging.INFO)

    # Version
    if args.version:
        logger.info("Client version " + client.version)
        logger.info("XRA-31 version " + client.server_version)

    # Commands
    if args.path and not args.wait_end and not args.wait_file_end:
        path = args.path
    else:
        path = client.capture.captured_path

    if args.wait_file_end:
        logger.info("Wait for a file rollover")
        path = client.capture.wait_for_file_end(timeout=args.timeout)
        if path:
            logger.info("Capture rollover, file {} ready".format(path))
        else:
            logger.warning("Failed waiting for file to rollover")
            sys.exit(1)
    elif args.wait_end:
        logger.info("Wait for the capture to end")
        path = client.capture.wait_for_end(timeout=args.timeout)
        if path:
            logger.info("Capture stopped, file {} ready".format(path))
        else:
            logger.warning("Failed waiting for capture to end")
            sys.exit(1)

    if args.download:
        logger.info("Download capture {}".format(path))
        try:
            client.analysis.download(path=path,
                                     output=args.output,
                                     append=args.append,
                                     rolling=args.rolling,
                                     compress=args.compress,
                                     verbose=not args.quiet)
        except exceptions.Xra31FileNotFoundException as error:
            logger.error("Could not download {} from {}: {}".format(
                path, args.address, str(error)))
            sys.exit(1)

    if args.delete:
        logger.info("Delete capture {}".format(path))
        try:
            client.analysis.delete(path=path,
                                   rolling=args.rolling,
                                   verbose=not args.quiet)
        except exceptions.Xra31FileNotFoundException as error:
            logger.error("Could not delete {} from {}: {}".format(
                path, args.address, str(error)))
            sys.exit(1)
