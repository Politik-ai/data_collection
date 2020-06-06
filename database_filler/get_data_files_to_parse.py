#!/usr/bin/env python3
from get_text_files_to_parse import get_bill_state_paths

congress_data_dir = '../../congress/data/'

# get all congress bills
def get_all_data_paths():

    bill_state_paths = get_bill_state_paths()

    bills = set()
    for bill_state in bill_state_paths:
        bills.add(bill_state[0] + '/bills/' + bill_state[1] + '/' + bill_state[1] + bill_state[2] + '/data.json')

    #print(bills)
    return list(bills)
