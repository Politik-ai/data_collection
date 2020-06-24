#!/usr/bin/env python3

from get_bill_states_to_parse import get_bill_state_paths
from get_data_file import get_data_path
import os


def all_high_level_data_files():
    all_bill_states = get_bill_state_paths()
    data_paths = set()

    for bs_path in all_bill_states:
        data_paths.add(get_data_path(bs_path))
    #print(list(data_paths))
    return list(data_paths)

all_high_level_data_files()