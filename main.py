import os
import sys
import argparse
import src.logger_setup as logger_setup
from src import train, predict
import importlib
import structlog

logger = structlog.get_logger()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Instantiating argparse object for a ds pipeline tutorial blog",
        epilog = "this will appear at the bottom of the --help message"
    )

    # adding arguments to our parser object
    parser.add_argument(
                "--train",
                action="store_true",
                help = "run through training phase",
            )
    parser.add_argument(
                "--predict",
                action="store_true",
                help = "run through prediction phase",  
            )
    parser.add_argument(
                "--local",
                action="store_true",
                help="for local testing only, will not write to database"
            )
    parser.add_argument(
                "--data_dir",
                help = "directory which data is stored and output",
                default="~/hotel_bookings"
            )
    parser.add_argument(
                "--log_level",
                help = "log level",
                default="INFO"
            )
    parser.add_argument(
                "--dev_mode",
                action="store_true",
                help = "to use pretty printing for logger"
            )


    ARGS = parser.parse_args()
    logger_setup.create_logger(ARGS)


    if ARGS.train:
        train.main(ARGS)

    if ARGS.predict:
        predict.main(ARGS)

    if not ARGS.train and not ARGS.predict:
        logger.error("Must pass a --train or --predict flag. Nothing to execute, exiting 👋")