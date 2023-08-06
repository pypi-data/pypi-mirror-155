#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from uuid import uuid4


def inject_annotation_to_data(export_data: List[Dict]) -> List[Dict]:
    # TODO: solve multi type of tasks
    return export_data


def convert_data(datas: List[Dict], set_uuid=False) -> List[Dict]:
    converted = []
    for data in datas:
        if set_uuid:
            data.update({"_id": uuid4().hex})
        data = {"data": data}
        converted += [data]
    return converted


def load_dataset(name: str, branch="main") -> List[Any]:
    # TODO: use mysql client interface
    return []
