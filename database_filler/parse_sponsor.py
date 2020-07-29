#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

from framework import Bill, Sponsorship, Politician


def add_sponsors(session, files, existing_bill_codes = []):

    relative_congress_loc = "../../congress/data/"
    num_sponsors = 0

    for f in files:
        path = relative_congress_loc + f + '/data.json'
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            continue
        with open(path) as x:
            data = json.load(x)
            sponsor_type = 'primary'
            bill_code = data['bill_id']

            if bill_code in existing_bill_codes:
                print('skipping')
                continue



            bill_id = session.query(Bill.id).filter(Bill.bill_code == bill_code).first()
            if bill_id is None:
                continue
            else:
                bill_id = bill_id[0]


            sponsor = data.get('sponsor', None)
            if not sponsor:
                print(f'no sponsor for {bill_code}')
                continue
            bioid = sponsor.get('bioguide_id', None)
            if not bioid:
                bioid = session.query(Politician.bioid).filter(Politician.thomas_id == sponsor['thomas_id']).first()[0]
                
            politician_id = session.query(Politician.id).filter(Politician.bioid == bioid).first()[0]
            #link and add to database
            if not bill_id or not politician_id:
                print('skipping')
                continue
            new_sponsorship = Sponsorship(bill_id,politician_id,sponsor_type)
            session.add(new_sponsorship)
            num_sponsors += 1

            for cosp in data['cosponsors']:
                
                sponsor_type = 'cosponsor'
                bioid = cosp.get('bioguide_id', None)
                if not bioid:
                    bioid = session.query(Politician.bioid).filter(Politician.thomas_id == cosp['thomas_id']).first()[0]
                politician_id = session.query(Politician.id).filter(Politician.bioid == bioid).first()[0]
                if not politician_id:
                    print('Skipping a sponsorship, can\'t find politician...')
                    continue
                new_sponsorship = Sponsorship(bill_id,politician_id,sponsor_type)
                session.add(new_sponsorship)
                num_sponsors += 1


    print(f"{num_sponsors} Sponsors Added")
    session.commit()

