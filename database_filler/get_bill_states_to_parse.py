#!/usr/bin/env python3
#create nested structure to comb through all bills and gather required information. 
import os

def get_bill_state_paths():

    congress_data_dir = '../../congress/data/'

    total_files = []
    i = 0 
    id_num = 0
    congresses = [f.name  for f in os.scandir(congress_data_dir) if f.is_dir()]
    for congress in congresses:
        cur_path_1 = congress_data_dir + congress + '/bills'
        bill_types = [f.name for f in os.scandir(cur_path_1) if f.is_dir()]

        for bill_type in bill_types:
            cur_path_2 = cur_path_1 + '/' + bill_type
            bill_nums = [f.name for f in os.scandir(cur_path_2) if f.is_dir()]

            for bill_num in bill_nums:
                cur_path_3 = cur_path_2 + '/' + bill_num
                id_num += 1
                if os.path.isdir(cur_path_3 + '/text-versions'):
                    bill_states = [f.name for f in os.scandir(cur_path_3 + '/text-versions') if f.is_dir()]
                    
                    for bill_state in bill_states:
                        cur_path_4 = cur_path_3 + '/text-versions/' + bill_state
                        cur_path_4 = cur_path_4[len(congress_data_dir):]
                        bill_num_only = ''.join(i for i in bill_num if i.isdigit())
                        bill_info = [id_num, congress, bill_type, bill_num_only, bill_state, cur_path_4]
                        total_files.append(bill_info)
                        i += 1
    return total_files
