import requests
import sys
from .api import search_by_artist
from .folders import get_folder_names
from .logic import compare
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('path', nargs='?', default="./")
    parser.add_argument('writepath', nargs='?',  default="./")
    parser.add_argument('-m', '--mode', nargs='?', default=0, type=int)
    parser.add_argument('-i', '--include', nargs='?', default='')
    args = parser.parse_args()

    if (args.verbose):
        print("Getting artist names...")
    names = get_folder_names(args.path)
    if (args.verbose):
        print(f"Found {len(names)} artists\nComparing  with chorus...")

    if (args.include != ''):
        compare(names, args.mode, args.writepath,
                args.verbose, args.include.split(','))
    else:
        compare(names, args.mode, args.writepath, args.verbose)
