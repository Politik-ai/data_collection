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

    bioid_pol_dict = {}
    bioguide_id_to_polid = session.query(Politician.bioid, Politician).all()
    for bioid, polid in bioguide_id_to_polid:
        bioid_pol_dict[bioid] = polid

    

    relative_congress_loc = "../../congress/data/"
    num_sponsors = 0

    sponsors_to_add = []
    cur_batch = 0
    total_files = len(files)
    file_ind = 0
    for f in files:
        path = relative_congress_loc + f + '/data.json'
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            continue
        with open(path) as x:
            data = json.load(x)


            file_ind += 1
            print(f'Sponsor file {file_ind}/{total_files}')

            bill_code = data['bill_id']

            if bill_code in existing_bill_codes:
                print('skipping bill, bill code already there')
                continue

            #Since bill has already been added, get it to build relations
            bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()
            if bill is None:
                continue

            sponsor = data.get('sponsor', None)
            if not sponsor:
                print(f'no sponsor for {bill_code} :(')
                continue
            
            #Grab bioid for marking, and try thomas ID if bioid not found
            bioid = sponsor.get('bioguide_id', None)
            if not bioid:
                print('querying')

                bioid = session.query(Politician.bioid).filter(Politician.thomas_id == sponsor['thomas_id']).first()[0]
                
            #Get pol for relation building
            pol = bioid_pol_dict[bioid]
            
            #link and add to database
            if not pol:
                print('Can\'t find politician for sponsorship')
                continue

            primary_sponsor = Sponsorship(bill.id, pol.id, 'primary')
            sponsors_to_add.append(primary_sponsor)
            cur_batch += 1
            num_sponsors += 1

            bill.sponsors.append(primary_sponsor)
            pol.sponsorships.append(primary_sponsor)

            for cosp in data['cosponsors']:
                
                bioid = cosp.get('bioguide_id', None)
                if not bioid:
                    print('querying')
                    bioid = session.query(Politician.id).filter(Politician.thomas_id == cosp['thomas_id']).first()[0]
                
                pol = bioid_pol_dict[bioid]

                if not pol:
                    print('Skipping a sponsorship, can\'t find politician...')
                    continue

                co_sponsor = Sponsorship(bill.id, pol.id, 'cosponsor')
                bill.sponsors.append(co_sponsor)
                pol.sponsorships.append(co_sponsor)
                sponsors_to_add.append(co_sponsor)

                num_sponsors += 1
                cur_batch += 1

                if cur_batch > 100000:
                    session.bulk_save_objects(sponsors_to_add)
                    session.commit()
                    cur_batch = 0
                    sponsors_to_add = []
                #print(f"Adding sponsor #{num_sponsors}/{total_files}")

    session.bulk_save_objects(sponsors_to_add)
    session.commit()
    print(f"{num_sponsors} Sponsors Added")

