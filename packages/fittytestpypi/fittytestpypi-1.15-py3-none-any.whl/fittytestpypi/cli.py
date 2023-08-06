#!/usr/bin/env python3

import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('argv is', argv)
    
    with open('billi.txt', 'r') as f:
        print(f.read())

    return 0
