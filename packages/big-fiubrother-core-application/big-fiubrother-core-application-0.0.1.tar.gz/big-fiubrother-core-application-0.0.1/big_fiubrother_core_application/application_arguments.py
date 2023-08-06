import argparse


def parse_arguments(application_name):
    parser = argparse.ArgumentParser(description=application_name)
    parser.add_argument('environment',
                        type=str,
                        nargs='?',
                        default='development',
                        help="Application environment. By default it's development.")

    return parser.parse_args()
