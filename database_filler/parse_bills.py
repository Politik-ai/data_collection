#!/usr/bin/env python3

from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import sys, os, csv, json
sys.path.insert(1, '../')
from get_bill_states_to_parse import get_bill_state_paths
from get_data_file import get_data_path

def insert_bills():

    files = get_bill_state_paths()
    cur_bill_id = -1
    for f in files:

        data_file = get_data_path(f)
        bill_data_path = relative_congress_loc + data_file + '/data.json'

        if f[0] != cur_bill_id:
            session.execute("INSERT INTO bills(bill_code) VALUES (:bill_code)", {"bill_code": f[2] + f[3]+ '-' + f[1]})
            cur_bill_id = session.execute(func.count(bills.c.id)).first().items()[0][1]

        bill_state_dict = {}

        #get titles from json, short and official
        #NOTE: should we get all short titles and of portions?
        with open(bill_data_path) as x:
            data = json.load(x)
            bill_state_dict["short_title"] = data['short_title']
            bill_state_dict["official_title"] = data['official_title']

        bill_state_dict["congress"] = f[1]
        bill_state_dict["bill_type"] = f[2]
        bill_state_dict["status_code"] = f[4]
        bill_state_dict['bill_state_identifier'] = f[2] + f[3] + f[4] + '-' + f[1]
        bill_state_dict["bill_id"] = cur_bill_id
        

        bill_state_dict["text_location"] = os.path.abspath(f[5] + "/document.txt")

        with open(relative_congress_loc + f[5] + '/data.json') as x:
            data = json.load(x)
            dob = data["issued_on"]
            bill_state_dict["intro_date"] = date(*[int(i) for i in dob.split('-')])

        session.execute(
            "INSERT INTO bill_states(bill_state_identifier, bill_id, bill_type, status_code, text_location, short_title, official_title, intro_date, congress) \
            VALUES (:bill_state_identifier, :bill_id, :bill_type, :status_code, :text_location, :short_title, :official_title, :intro_date, :congress)",
            bill_state_dict)

    session.commit()

if __name__ == "__main__":

    engine = create_engine('sqlite:///../political_db.db')
    session = scoped_session(sessionmaker(bind=engine))
    relative_congress_loc = "../../congress/data/"

    meta = MetaData()
    bills = Table(
        'bills', meta,
        Column('id', Integer, primary_key=True),
        Column('bill_code', String),
        sqlite_autoincrement=True
    )

    bill_states = Table(
        'bill_states', meta,
        Column('id', Integer, primary_key=True),
        Column('bill_state_identifier', String),
        Column('bill_id', Integer),
        Column('bill_type', String),
        Column('status_code', String),
        Column('text_location', String),
        Column('short_title', String),
        Column('official_title', String),
        Column('intro_date', Date),
        Column('congress', Integer),
        sqlite_autoincrement=True
    )

    meta.create_all(engine)
    insert_bills()
