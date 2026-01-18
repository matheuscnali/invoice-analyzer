import argparse
from pathlib import Path

from .analyzer import analyze
from .custom_types import Config
from .parsers import parse_invoice
from .report import generate_report
from .utils.fs import read_yaml
from .utils.log import info, print_dash

VERSION = '0.0.0'

def get_config(config_filepath: Path) -> Config:
    info('  - Processing configuration')
    config = read_yaml(config_filepath)
    return Config(**config)


def main():
    parser = argparse.ArgumentParser(description='A bank invoice analyzer')
    parser.add_argument('--config_filepath', type=Path)
    parser.add_argument('--version', action='store_true')
    args = parser.parse_args()

    if args.version:
        print(f'Invoice analyzer version: {VERSION}')
        exit(0)

    if args.config_filepath is None:
        parser.print_usage()
        exit(1)

    print_dash()
    info(f'Welcome to Invoice Analyzer v{VERSION}')

    config = get_config(args.config_filepath)
    invoice = parse_invoice(config.invoice_filepath, config.invoice_source)
    analysis = analyze(invoice, config)
    generate_report(analysis, config, VERSION)

    info('  - All done!')
    print_dash()


if __name__ == '__main__':
    main()
