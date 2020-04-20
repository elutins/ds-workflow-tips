import argparse
import logger_setup

logger = logger_setup.new()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Instantiating argparse object')

    # adding arguments to our parser object
    parser.add_argument('--training',
                        action='store_true',
                        help = 'run through training phase',
                )
    parser.add_argument('--predict',
                        action='store_true',
                        help = 'run through prediction phase',  
                )
    parser.add_argument('--local',
                    action='store_true',
                    help='for local testing only, will not write to database'
                )
    parser.add_argument('--data_dir',
                    help = 'directory which data is stored',
                )


ARGS = parser.parse_args()

logger = logger.initialize(level=ARGS.level)