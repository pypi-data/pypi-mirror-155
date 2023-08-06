#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataops_toolkits.io import read_json, dump_json
from dataops_toolkits.utils import convert_data

import argparse


def convert(source: str, target: str, set_uuid=False):
    datas = read_json(source, per_line_mode=True)

    if datas is not None:
        datas = convert_data(datas, set_uuid=set_uuid)  # type:ignore
        dump_json(datas, target, per_line_mode=False)
    else:
        raise Exception("Invalid Data")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--source", type=str, required=True, help="source file path"
    )
    parser.add_argument(
        "-t", "--target", type=str, required=True, help="target file path"
    )
    parser.add_argument("--set_id", action="store_true", help="set id for data or not")

    args = parser.parse_args()

    return convert(args.source, args.target, args.set_id)


if __name__ == "__main__":
    main()
