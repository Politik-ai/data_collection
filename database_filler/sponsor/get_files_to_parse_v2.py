#!/usr/bin/env python3

import os

congress_data_dir = '/home/beth/congress/data/'


# get all congress bills
def get_all_paths():

    total_files = []
    i = 0
    congresses = [f.name for f in os.scandir(congress_data_dir) if f.is_dir()]
    for congress in congresses:
        cur_path_1 = congress_data_dir + congress + '/bills'
        bill_types = [f.name for f in os.scandir(cur_path_1) if f.is_dir()]

        for bill_type in bill_types:
            cur_path_2 = cur_path_1 + '/' + bill_type
            bill_nums = [f.name for f in os.scandir(cur_path_2) if f.is_dir()]

            for bill_num in bill_nums:
                cur_path_3 = cur_path_2 + '/' + bill_num
                cur_path_4 = cur_path_3 + '/data.json'
                bill_num_only = ''.join(i for i in bill_num if i.isdigit())
                bill_info = [congress, bill_type, bill_num_only, cur_path_4]
                total_files.append(bill_info)
                i += 1
    print(f'total number of files: {i}')
    # 48991
    return total_files
