#!/usr/bin/env python3

from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql, func
import os, json
from get_data_file import get_data_path

from base import Session, engine, Base
from framework import Bill, Bill_State


def add_bills_and_bill_states(session, files, existing_bill_codes = [], existing_bill_state_identifiers = []):


    relative_congress_loc = "../../congress/data/"
    cur_bill_id = -1
    num_bills, num_bill_states = 0, 0

    for f in files:

        data_file = get_data_path(f)

        bill_data_path = relative_congress_loc + data_file + '/data.json'

        data = None
        if f[0] != cur_bill_id:
            bill_code = f[2] + f[3]+ '-' + f[1]
            originating_body = f[2]

            if os.path.isfile(bill_data_path):
                with open(bill_data_path) as x:
                    data = json.load(x)
                    status = data['status']
            else:
                status = None

            if not (bill_code in existing_bill_codes):
                cur_bill = Bill(bill_code, status, originating_body)
                session.add(cur_bill)
                num_bills += 1
            else:
                cur_bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()


    
        #get titles from json, short and official if exists
        if os.path.isfile(bill_data_path):

            bill_state_identifier = f[2] + f[3] + f[4] + '-' + f[1]

            #Don't add existing bill_states if already there
            if bill_state_identifier in existing_bill_state_identifiers:
                continue

            congress = f[1]
            bill_type = f[2]
            status_code = f[4]
            text_location = os.path.abspath(f[5] + "/document.txt")

            #Grab Bill_State titles from general data file
            with open(bill_data_path) as x:
                if not data:
                    data = json.load(x)
                short_title = data['short_title']
                official_title = data['official_title']

            #Look for specific json file to find bill state dates
            if os.path.isfile(relative_congress_loc + f[5] + '/data.json'):

                with open(relative_congress_loc + f[5] + '/data.json') as x:
                    data = json.load(x)
                    dob = data["issued_on"]
                    intro_date = date(*[int(i) for i in dob.split('-')])

                bill_state_info = [cur_bill,cur_bill.id,bill_state_identifier,bill_type,status_code, \
                    text_location,short_title,official_title,intro_date,congress]

                new_bill_state = Bill_State(*bill_state_info)
                cur_bill.bill_states.append(new_bill_state)
                num_bill_states += 1
                print(f'added bill state {num_bill_states}')
            else:
                print(f"bill_state json {relative_congress_loc + f[5] + '/data.json'} not found")
                continue
        else:
            print(f'bill json {bill_data_path} not found')
            continue

    session.commit()
    print(f"{num_bills} Bill Added")
    print(f"{num_bill_states} Bill States Added")
