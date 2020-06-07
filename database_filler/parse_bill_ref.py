#!/usr/bin/env python3
import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker


def main():

    engine = create_engine('sqlite:///../political_db.db', echo=True)
    db = scoped_session(sessionmaker(bind=engine))
    relative_congress_loc = "../../congress/data/"
    engine = create_engine('sqlite:///../political_db.db', echo=True)
    meta = MetaData()

    bill_ref = Table(
        'bill_ref', meta,
        Column('id', Integer, primary_key=True),
        Column('to_bill', String),
        Column('from_bill', String),
        sqlite_autoincrement=True
    )


    meta.create_all(engine)
    conn = engine.connect()
    conn.execute(bill_ref.delete())
    conn.execute(bill_ref.delete())

    files = all_high_level_data_files()
    for f in files:
        path = relative_congress_loc + f + '/data.json'
        #print(f)
        path = os.path.abspath(path)
        #print(path)
        with open(path) as x:
            data = json.load(x)
            
            from_bill = data['bill_id']

            for related in data['related_bills']:
                to_bill = related['bill_id']

                ins = bill_ref.insert().values(to_bill=to_bill, from_bill=from_bill)
                db.execute(ins)
    db.commit()


#just making sure this works
if __name__ == "__main__":
    main()
