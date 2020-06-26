#!/usr/bin/env python3

from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql, func
import os, json
from get_bill_states_to_parse import get_bill_state_paths
from get_data_file import get_data_path

from base import Session, engine, Base
from framework import Bill, Bill_State

Base.metadata.create_all(engine)
session  = Session()

relative_congress_loc = "../../congress/data/"

files = get_bill_state_paths()
cur_bill_id = -1
num_bills, num_bill_states = 0, 0
for f in files:
    data_file = get_data_path(f)
    bill_data_path = relative_congress_loc + data_file + '/data.json'

    if f[0] != cur_bill_id:
        bill_code = f[2] + f[3]+ '-' + f[1]
        originating_body = f[2]
        if os.path.isfile(bill_data_path):
            with open(bill_data_path) as x:
                data = json.load(x)
                status = data['status']
        else:
            status = None
        new_bill = Bill(bill_code, status, originating_body)
        session.add(new_bill)
        num_bills += 1
        cur_bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()
        cur_bill_id = f[0]  
        #print(f'added bill {cur_bill_id}')
  
    #get titles from json, short and official
    if os.path.isfile(bill_data_path):
        with open(bill_data_path) as x:
            if not data:
                data = json.load(x)
            short_title = data['short_title']
            official_title = data['official_title']

        congress = f[1]
        bill_type = f[2]
        status_code = f[4]
        bill_state_identifier = f[2] + f[3] + f[4] + '-' + f[1]
        text_location = os.path.abspath(f[5] + "/document.txt")

        if os.path.isfile(relative_congress_loc + f[5] + '/data.json'):
            with open(relative_congress_loc + f[5] + '/data.json') as x:
                data = json.load(x)
                dob = data["issued_on"]
                intro_date = date(*[int(i) for i in dob.split('-')])

            bill_state_info = [cur_bill,cur_bill.id,bill_state_identifier,bill_type,status_code, \
                text_location,short_title,official_title,intro_date,congress]

            new_bill_state = Bill_State(*bill_state_info)
            session.add(new_bill_state)
            num_bill_states += 1
            #print(f'added bill state {num_bill_states}')
        else:
            #print(f"bill_state json {relative_congress_loc + f[5] + '/data.json'} not found")
            continue
    else:
        print(f'bill json {bill_data_path} not found')
        continue


print(f"{num_bills} Bill Added")
print(f"{num_bill_states} Bill States Added")
session.commit()

