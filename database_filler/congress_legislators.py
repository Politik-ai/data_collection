#AIM: to get all relevant information on all legislators into database

#parse through yamls
import yaml
import os
from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql
import csv
engine = create_engine('sqlite:///politician_term.db', echo = True)
meta = MetaData()

politician_term = Table(
   'politician_term', meta, 
   Column('id', Integer, primary_key = True),
   Column('polid', Integer), 
   Column('firstname', String), 
   Column('lastname', String), 
   Column('start', Date),
   Column('end', Date),
   Column('party_affiliation', String),
   Column('state', String),
   Column('legislative_body', String),
   Column('gender', String),
   Column('district', String),
   sqlite_autoincrement=True
)

politician = Table(
    'politician', meta,
    Column('id', Integer, primary_key = True),
    Column('date_of_birth', Date),
    Column('race', String)
)

meta.create_all(engine)

conn = engine.connect()

current_yaml = 'congress-legislators/legislators-current.yaml'
historical_yaml = 'congress-legislators/legislators-historical.yaml'
congress_dir = '../../congress/'
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, congress_dir + current_yaml)

#open up the yaml files
with open(congress_dir + current_yaml) as file:
    info = yaml.full_load(file)
    #print(info)
    for item in info:
        
        gender = item['bio']['gender']
        dob = item['bio']['birthday']
        bioid = item['id']['bioguide']
        firstname = item['name']['first']
        lastname = item['name']['last']
        ins = politician.insert().values(id = bioid, date_of_birth = dob)
        for term in item['terms']:
            start_date = date(*[int(i) for i in term['start'].split('-')])
            end_date = date(*[int(i) for i in term['end'].split('-')])
            party = term['party']
            body = term['type']
            state = term['state']
            district = None
            if body == 'rep':
                district = term['district']

            ins = politician_term.insert().values(polid = bioid, firstname = firstname, lastname = lastname, \
            party_affiliation= party, state = state, district = district, start = start_date, end = end_date, \
            legislative_body = body, gender = gender)
            result = conn.execute(ins)
            
meta.bind = engine

s = politician_term.select()
conn.engine.connect()
result = conn.execute(s)
fh = open('pol_db.csv', 'wb')
outcsv = csv.writer(fh)
outcsv.writerow(result.keys())
for row in result:
    print('test')
    print(row)
outcsv.writerows(result)
fh.close
