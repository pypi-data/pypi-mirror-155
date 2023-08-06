#!/usr/bin/env python3
"""
Command-line interface to :class:`~excentis.xra31.configuration.Configuration`.
"""

# pylint: disable=logging-format-interpolation
# pylint: disable=logging-not-lazy

import argparse
import json
import logging
import os
import pathlib
import sys

from .. import ChannelState, connect, exceptions, tracer, version

# Arguments
parser = argparse.ArgumentParser(
    description="Configure the XRA-31 channels.  "
    "The three commands can be combined, and will be executed in the order "
    "store, load, wait-lock.")

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
    metavar="channels.json",
    help="store the current XRA-31 channel configuration to JSON",
    type=str)
parser_commands.add_argument(
    "--load",
    metavar="channels.json",
    help="load a JSON channel configuration to the XRA-31",
    type=argparse.FileType('r'))
parser_commands.add_argument("--wait-lock",
                             action="store_true",
                             help="wait for all channels to be locked")

parser_options = parser.add_argument_group("command options")
parser_options.add_argument(
    "-t",
    "--timeout",
    help="maximum time to wait for lock and channel detection (seconds)",
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
    if args.store:
        logger.info("Store configuration in " + args.store)
        try:
            description = client.configuration.describe()
            with (sys.stdout
                  if args.store == "-" else open(args.store, "w")) as file:
                json.dump(description, file, indent=4)
        except OSError as error:
            logger.error("Could not write to " + args.store + ": " +
                         str(error))
            sys.exit(1)
        except exceptions.Xra31Exception as error:
            logger.error("Could not store channel configuration: " +
                         str(error))
            sys.exit(1)

    if args.load:
        # Ensure full access available
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

        # Verify capture activity
        if client.capture.active:
            logger.error(
                "Channel configuration can not be changed while capturing")
            sys.exit(1)
        with client:
            logger.info("Load configuration from " + args.load.name)
            description = json.load(args.load)
            try:
                client.configuration.apply(description, timeout=args.timeout)
            except exceptions.Xra31Exception as error:
                logger.error("Could not load channel configuration: " +
                             str(error))
                sys.exit(1)

    if args.wait_lock:
        for channel in client.configuration:
            if channel.state != ChannelState.LOCKED:
                logger.info("Wait for {} to lock...".format(str(channel)))
                if not client.configuration.wait_for_state(
                        channel, state=ChannelState.LOCKED,
                        timeout=args.timeout):
                    logger.warning(
                        "Timeout while waiting for {} to lock".format(
                            str(channel)))
                    sys.exit(1)
            logger.info("{} locked".format(str(channel)))
