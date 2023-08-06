import argparse
from datetime import datetime

class HiveDateAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            d = datetime.strptime(values, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date {values} not in proper format")

        print('%r %r %r' % (namespace, d, option_string))
        setattr(namespace, self.dest, d)

def process_etl_arguments(args):
    parser = argparse.ArgumentParser(description='Process data from the given period')
    parser.add_argument('-start_date', metavar='Start date', type=str, action=HiveDateAction,
                    help='the minimum date to process')
    parser.add_argument('-end_date', metavar='Start date', type=str, action=HiveDateAction,
                    help='the maximum data to process)')

    return parser.parse_args(args)