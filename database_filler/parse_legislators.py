#!/usr/bin/env python3

# AIM: to get all relevant information on all legislators into database

# parse through yamls
import yaml
import os
from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker
import csv

engine = create_engine('sqlite:///../political_db.db')
meta = MetaData()

politician_term = Table(
    'politician_term', meta,
    Column('id', Integer, primary_key=True),
    Column('bioid', String),
    Column('polid', Integer),
    Column('firstname', String),
    Column('lastname', String),
    Column('start_date', Date),
    Column('end_date', Date),
    Column('party_affiliation', String),
    Column('state', String),
    Column('legislative_body', String),
    Column('gender', String),
    Column('district', String),
    sqlite_autoincrement=True
)


politician = Table(
    'politician', meta,
    Column('id', Integer, primary_key=True),
    Column('bioid', String),
    Column('date_of_birth', Date),
    # Column('race', String),
    sqlite_autoincrement=True
)

leadership_roles = Table(
    'leadership_roles', meta,
    Column('id', Integer, primary_key=True),
    Column('bioid', String),
    Column('polid', Integer),
    Column('role', String),
    Column('chamber', String),
    Column('start_date', Date),
    Column('end_date', Date),
    sqlite_autoincrement = True
)


meta.create_all(engine)
conn = engine.connect()
conn.execute(politician_term.delete())
conn.execute(politician.delete())
sess = sessionmaker()
sess.configure(bind=engine)
session = sess()


current_yaml = 'congress-legislators/legislators-current.yaml'
historical_yaml = 'congress-legislators/legislators-historical.yaml'
congress_dir = '../../congress/'
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, congress_dir + current_yaml)
skips = 0
# open up the yaml files
for y in [current_yaml, historical_yaml]:
    with open(congress_dir + y) as file:
        info = yaml.full_load(file)
        for item in info:
            gender = item['bio']['gender']
            dob = item['bio'].get('birthday', '0001-01-01')
            dob = date(*[int(i) for i in dob.split('-')])
            if dob.year < 1900:
                skips += 1
                continue
            bioid = item['id']['bioguide']
            firstname = item['name']['first']
            lastname = item['name']['last']
            pol = politician.insert().values(date_of_birth=dob, bioid=bioid)
            result = session.execute(pol)
            pol_id = session.execute(func.count(politician.c.id)).first().items()[0][1]

            #Adding Politiican Terms
            for term in item['terms']:
                start_date = date(*[int(i) for i in term['start'].split('-')])
                end_date = date(*[int(i) for i in term['end'].split('-')])
                if end_date.year < 1950:
                    continue
                party = term.get('party', "NA")
                body = term['type']
                state = term['state']
                district = None
                if body == 'rep':
                    district = term['district']
                ins = politician_term.insert().values(polid=pol_id, bioid=bioid, firstname=firstname, lastname=lastname,
                                                      party_affiliation=party, state=state, district=district, start_date=start_date, end_date=end_date,
                                                      legislative_body=body, gender=gender)
                result = session.execute(ins)
            
            #Adding leadership roles
            if 'leadership_roles' in item:
                print('found roles')
                for role in item['leadership_roles']:
                    print('adding roles')
                    start = date(*[int(i) for i in role['start'].split('-')])

                    end = date(*[int(i) for i in role['end'].split('-')]) if 'end' in role else None
                    ins = leadership_roles.insert().values(bioid=bioid, polid=pol_id, role = role['title'], chamber = role['chamber'], start_date=start, end_date=end)
                    session.execute(ins)
meta.bind = engine
session.commit()
#print(skips)

# result = session.execute(politician_term.select())
# # result = conn.execute(s)
# if os.path.exists("pol_term.csv"):
#     os.remove("pol_term.csv")
# fh = open('pol_term.csv', 'w')
# outcsv = csv.writer(fh)
# outcsv.writerow([s for s in result.keys()])
# for row in result:
#     outcsv.writerow([s for s in row])
# fh.close

# result = session.execute(politician.select())
# if os.path.exists("pol.csv"):
#     os.remove("pol.csv")
# fh = open('pol.csv', 'w')
# outcsv = csv.writer(fh)
# outcsv.writerows(result.keys())
# for row in result:
#     outcsv.writerow(row)
# fh.close
