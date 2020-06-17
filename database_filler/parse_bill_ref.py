#!/usr/bin/env python3
from get_all_data_files import all_high_level_data_files
import json
import os
from sqlalchemy import Table, Column, Integer, String

from base import Session, engine, Base
from framework import Bill_Reference, Bill

Base.metadata.create_all(engine)
session  = Session()

relative_congress_loc = "../../congress/data/"

files = all_high_level_data_files()
ref_num = 0
for f in files:
    path = relative_congress_loc + f + '/data.json'
    with open(path) as x:
        data = json.load(x)
        
        from_bill = session.query(Bill).filter(Bill.bill_code == data['bill_id']).first()

        for related in data['related_bills']:
            to_bill = session.query(Bill).filter(Bill.bill_code == related['bill_id']).first()
            if to_bill is not None:
                ref_num += 1
                bill_ref = Bill_Reference(from_bill.id,to_bill.id)
                session.add(bill_ref)

print(f'References Added: {ref_num}')
session.commit()
