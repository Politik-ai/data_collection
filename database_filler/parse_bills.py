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
for f in files:

    data_file = get_data_path(f)
    bill_data_path = relative_congress_loc + data_file + '/data.json'

    if f[0] != cur_bill_id:
        bill_code = f[2] + f[3]+ '-' + f[1]
        #print(bill_code)
        new_bill = Bill(bill_code)
        session.add(new_bill)
        cur_bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()
        #print(cur_bill.id)


    #get titles from json, short and official
    with open(bill_data_path) as x:
        data = json.load(x)
        short_title = data['short_title']
        official_title = data['official_title']

    congress = f[1]
    bill_type = f[2]
    status_code = f[4]
    bill_state_identifier = f[2] + f[3] + f[4] + '-' + f[1]

    text_location = os.path.abspath(f[5] + "/document.txt")

    with open(relative_congress_loc + f[5] + '/data.json') as x:
        data = json.load(x)
        dob = data["issued_on"]
        intro_date = date(*[int(i) for i in dob.split('-')])

    bill_state_info = [cur_bill,cur_bill.id,bill_state_identifier,bill_type,status_code, \
        text_location,short_title,official_title,intro_date,congress]

    new_bill_state = Bill_State(*bill_state_info)
    session.add(new_bill_state)

session.commit()

