#!/usr/bin/python


def get_version():
    return "0.5"


def _load_data():
    import os
    import json

    path= os.path.dirname(__file__)
    with open(f'{path}/data/institutions.json') as f:
        coll = json.load(f)
    return coll


def get_institutes():
    return _load_data()


def _parser():
    import argparse

    parser = argparse.ArgumentParser(description='Pakistani radio station player.')

    parser.add_argument('-i', '--institutes', action=argparse.BooleanOptionalAction, default=False,
            help='List all available institutions.')
    parser.add_argument('-v', '--version', action=argparse.BooleanOptionalAction, default=False,
            help='Show application version.')

    args = parser.parse_args()
    return args


def _main():
    args = _parser()
    
    if args.version:
        print(f'\033[1m{get_version()}\033[0m')
    elif args.institutes:
        insts = get_institutes()
        for inst in insts:
            for k,v in inst.items():
                print(f'\033[2m{k.capitalize()}\033[0m {v}')
            print('---\n')


if __name__ == '__main__':
    _main()
