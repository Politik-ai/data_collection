#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

from base import Session, engine, Base
from framework import Bill, Sponsorship, Politician

Base.metadata.create_all(engine)
session  = Session()
relative_congress_loc = "../../congress/data/"


files = all_high_level_data_files()

for f in files:
    path = relative_congress_loc + f + '/data.json'
    path = os.path.abspath(path)
    with open(path) as x:
        data = json.load(x)
        sponsor_type = 'primary'
        #state = data['sponsor']['state']
        #title = data['sponsor']['title']
        bill_code = data['bill_id']
        bill_id = session.query(Bill.id).filter(Bill.bill_code == bill_code).first()[0]
        bioid = data['sponsor']['bioguide_id']
        politician_id = session.query(Politician.id).filter(Politician.bioid == bioid).first()[0]
        # link and add to database
        if not bill_id or not politician_id:
            print('skipping')
            continue
        new_sponsorship = Sponsorship(bill_id,politician_id,sponsor_type)
        session.add(new_sponsorship)

        for cosp in data['cosponsors']:
            sponsor_type = 'cosponsor'
            bioid = cosp['bioguide_id']
            politician_id = session.query(Politician.id).filter(Politician.bioid == bioid).first()
            if not politician_id:
                print('skipping a sponsorship, can\'t find politician')
            continue
            new_sponsorship = Sponsorship(bill_id,politician_id,sponsor_type)
            session.add(new_sponsorship)


session.commit()

