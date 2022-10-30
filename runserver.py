#!/usr/bin/env python3.10

import argparse
from sys import argv, stderr, exit
from yalepapp import app

def main():
    args = parse_args()
    try:
        port = int(vars(args)['port'])
    except Exception:
        print('Port must be an integer.', file=stderr)
        exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def parse_args():
    '''
    parses arguments and returns a dict
    '''
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('port', help='the port at which the server should listen')
    return parser.parse_args()

if __name__ == '__main__':
    main()
