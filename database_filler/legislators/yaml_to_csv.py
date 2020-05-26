#AIM: to get all relevant information on all legislators into database

#parse through yamls
import yaml
import os
from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql
from sqlalchemy.orm import sessionmaker
import csv
from sqlalchemy.ext.declarative import declarative_base

"""
Base = declarative_base()
class politician(Base):
    __tablename__ = 'politician'
    id = Column(Integer, primary_key = True)
    bioid = Column(String)
    date_of_birth = Column(Date)

    def __repr__(self):
        return "<politician(name="
"""




engine = create_engine('sqlite:///politician_term.db', echo = True)
meta = MetaData()

politician_term = Table(
   'politician_term', meta, 
   Column('id', Integer, primary_key = True),
   Column('polid', String), 
   Column('firstname', String), 
   Column('lastname', String), 
   Column('start_d', Date),
   Column('end_d', Date),
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
    Column('bioid', String),
    Column('date_of_birth', Date),
    #Column('race', String),
    sqlite_autoincrement=True
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
congress_dir = '../../../congress/'
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, congress_dir + current_yaml)
skips = 0
#open up the yaml files
for y in [current_yaml, historical_yaml]:
    with open(congress_dir + y) as file:
        info = yaml.full_load(file)
        for item in info:
            gender = item['bio']['gender']
            dob = item['bio'].get('birthday','0001-01-01')
            dob = date(*[int(i) for i in dob.split('-')])
            if dob.year < 1900:
                skips += 1
                continue
            bio_id = item['id']['bioguide']
            firstname = item['name']['first']
            lastname = item['name']['last']
            pol = politician.insert().values(date_of_birth = dob, bioid = bio_id)
            result = session.execute(pol)
            for term in item['terms']:
                start_date = date(*[int(i) for i in term['start'].split('-')])
                end_date = date(*[int(i) for i in term['end'].split('-')])
                if end_date.year < 1950:
                    continue
                party = term.get('party',"NA")
                body = term['type']
                state = term['state']
                district = None
                if body == 'rep':
                    district = term['district']
                ins = politician_term.insert().values(polid = bio_id, firstname = firstname, lastname = lastname, \
                party_affiliation= party, state = state, district = district, start_d = start_date, end_d = end_date, \
                legislative_body = body, gender = gender)
                result = session.execute(ins)
                

print(skips)
meta.bind = engine

result = session.execute(politician_term.select())
#result = conn.execute(s)
if os.path.exists("pol_term.csv"):
    os.remove("pol_term.csv")
fh = open('pol_term.csv', 'wb')
outcsv = csv.writer(fh)
outcsv.writerow(result.keys())
for row in result:
    outcsv.writerow([unicode(s).encode("utf-8") for s in row])
fh.close

result = session.execute(politician.select())
if os.path.exists("pol.csv"):
    os.remove("pol.csv")
fh = open('pol.csv', 'wb')
outcsv = csv.writer(fh)
outcsv.writerow(result.keys())
for row in result:
    outcsv.writerow([unicode(s).encode("utf-8") for s in row])
fh.close
