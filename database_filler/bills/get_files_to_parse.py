#!/usr/bin/env python3
#create nested structure to comb through all bills and gather required information. 
import os

congress_data_dir = '../../../congress/data/'


#get all congress bills
def get_all_paths():
    total_files = []

    congresses = [f.path + '/bills/' for f in os.scandir(congress_data_dir) if f.is_dir()]
    bill_types = []
    for congress in congresses:
        bill_types = [f.path for f in os.scandir(congress) if f.is_dir()]
        for bill_type in bill_types:
            bill_nums = [f.path for f in os.scandir(bill_type) if f.is_dir()]
            for bill_num in bill_nums:
                print(bill_num)
                bill_states = [f.path for f in os.scandir(bill_num) if f.is_dir()]
                for bill_state in bill_states:
                    print(bill_states)

    return total_files


if __name__ == "__main__":
    files = get_all_paths()
    print(files)