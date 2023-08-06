#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json


def main():
    args, _ = get_args()
    if args.version:
        from .__version__ import __version__
        print(__version__)


def get_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", action='store_true')

    args, unknow_args = parser.parse_known_args()

    return args, unknow_args


if __name__ == '__main__':
    main()
