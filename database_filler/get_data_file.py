#!/usr/bin/env python3

# get all congress bills
def get_data_path(bill_state_path):

    data_path = bill_state_path[1] + '/bills/' + bill_state_path[2] + '/' + bill_state_path[2] + bill_state_path[3]

    return data_path
