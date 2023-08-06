#!/usr/bin/env python3
"""
Command-line interface to :class:`~excentis.xra31.capture.Capture`.
"""

# pylint: disable=logging-format-interpolation
# pylint: disable=logging-not-lazy

import argparse
import json
import logging
import os
import pathlib
import sys

from .. import connect, exceptions, tracer, version

# Arguments
parser = argparse.ArgumentParser(
    description="Configure the XRA-31 capture.  "
    "The commands can be combined, and will be executed in the order "
    "store, load, start, stop, wait (end or file-end).  "
    "Command-line output options override configurations in the loaded file.")

parser.add_argument("address",
                    metavar="XRA-31",
                    help="XRA-31 hostname or IP address",
                    nargs="?")

parser.add_argument("-f",
                    "--force",
                    action="store_true",
                    help="force full access mode if it's in use")
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
parser_commands.add_argument(
    "--store",
    metavar="capture.json",
    help="store the current XRA-31 capture configuration to JSON "
    "(channels, filtering, output)",
    type=str)
parser_commands.add_argument(
    "--load",
    metavar="capture.json",
    help="load a JSON capture configuration to the XRA-31",
    type=argparse.FileType('r'))
parser_commands.add_argument("--start",
                             action="store_true",
                             help="start capturing")
parser_commands.add_argument("--stop",
                             action="store_true",
                             help="stop capturing")
parser_commands.add_argument("--wait-end",
                             action="store_true",
                             help="wait for the capture to end")
parser_commands.add_argument(
    "--wait-file-end",
    action="store_true",
    help="wait for the next file rollover in a rolling file capture")

parser_output = parser.add_argument_group("output")
parser_output.add_argument("-p",
                           "--path",
                           metavar="directory/capture.pcap",
                           help="capture path on the XRA-31",
                           type=pathlib.PurePosixPath)
parser_output.add_argument("--filename",
                           action="store_true",
                           help=argparse.SUPPRESS)
parser_output.add_argument("-D",
                           "--duration",
                           help="duration limit of the capture (seconds).  "
                           "0 for unlimited",
                           type=float)
parser_output.add_argument("-S",
                           "--size",
                           help="size limit of the capture (MB).  "
                           "0 for unlimited",
                           type=float)
parser_rolling = parser.add_argument_group("rolling file")
parser_rolling.add_argument("-n",
                            "--number-of-files",
                            help="number of files in the rolling file capture "
                            "(1 for single file capture)",
                            type=int)
parser_rolling.add_argument("-d",
                            "--file-duration",
                            help="per-file duration limit (seconds).  "
                            "0 for unlimited",
                            type=float)
parser_rolling.add_argument("-s",
                            "--file-size",
                            help="per-file size limit (MB).  "
                            "0 for unlimited",
                            type=float)

parser_options = parser.add_argument_group("command options")
parser_options.add_argument(
    "-t",
    "--timeout",
    help="maximum time to wait for the end of the capture "
    "or the rollover of a file (seconds)",
    type=float)


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

    configure_output = (
        args.path  #
        or args.duration is not None or args.size is not None  #
        or args.number_of_files is not None or args.file_duration is not None
        or args.file_size is not None)

    # Ensure full access available if needed
    if (args.load or args.start or args.stop  #
            or configure_output):
        if not args.force:
            if not client.try_full_access():
                logger.error(
                    "Request for full access failed: "
                    "verify if no scripts or the web interface are in "
                    "full access mode, "
                    "or force full access with the option --force")
                sys.exit(1)
        else:
            try:
                with client:
                    pass
            except exceptions.Xra31Exception as error:
                logger.error("Could not get exclusive access to the XRA-31: " +
                             str(error))
                sys.exit(1)

    # Verify capture activity if needed
    if (args.load or args.start  #
            or configure_output):
        if client.capture.active:
            logger.error("Capture can not be changed while capturing")
            sys.exit(1)

    # Version
    if args.version:
        logger.info("Client version " + client.version)
        logger.info("XRA-31 version " + client.server_version)

    # Commands
    if args.store:
        logger.info("Store configuration in " + args.store)
        try:
            description = client.capture.describe()
            with (sys.stdout
                  if args.store == "-" else open(args.store, "w")) as file:
                json.dump(description, file, indent=4)
        except OSError as error:
            logger.error("Could not write to " + args.store + ": " +
                         str(error))
            sys.exit(1)
        except exceptions.Xra31Exception as error:
            logger.error("Could not store capture configuration: " +
                         str(error))
            sys.exit(1)

    description = {}
    if args.load:
        logger.info("Load configuration from " + args.load.name)
        description = json.load(args.load)
    else:
        from ..capture import JSON_CLIENT_VERSION
        description["min_client_version"] = JSON_CLIENT_VERSION

    if configure_output:
        if "output" not in description:
            description["output"] = {}
        output = description["output"]

        if args.path is not None:
            output["path"] = args.path or None

        if args.duration is not None:
            output["duration"] = args.duration or None
        if args.size is not None:
            output["size"] = args.size or None
        if args.number_of_files is not None:
            output["number_of_files"] = (args.number_of_files
                                         if args.number_of_files > 1 else None)
        if args.file_duration is not None:
            output["file_duration"] = args.file_duration or None
        if args.file_size is not None:
            output["file_size"] = args.file_size or None

    if (args.load or configure_output):
        logger.info("Configure capture")
        with client:
            try:
                client.capture.apply(description)
            except exceptions.Xra31Exception as error:
                logger.error("Could not load capture configuration: " +
                             str(error))
                sys.exit(1)

    if args.start:
        with client:
            logger.info("Start capture")
            client.capture.start()

    if args.stop:
        with client:
            logger.info("Stop capture")
            client.capture.stop()

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
