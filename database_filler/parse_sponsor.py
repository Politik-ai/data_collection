import sys
sys.path.insert(1, '../')
from get_data_files_to_parse import get_all_data_paths
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

def insert_sponsors():
    files = get_all_data_paths()

    for f in files:
        path = relative_congress_loc + f
        print(f)
        path = os.path.abspath(path)
        print(path)
        with open(path) as x:
            data = json.load(x)
            sponsor_type = 'primary'
            state = data['sponsor']['state']
            title = data['sponsor']['title']
            bill_state_id = data['bill_id']
            politician_id = data['sponsor']['bioguide_id']
            # link and add to database
            db.execute(
                "INSERT INTO sponsorship(sponsor_type, bill_state_id, politician_id) VALUES (:sponsor_type, :bill_state_id, :politician_id)",
                {"sponsor_type": sponsor_type, "bill_state_id": bill_state_id, "politician_id": politician_id}
            )

            for cosp in data['cosponsors']:
                sponsor_type = 'cosponsor'
                state = cosp['state']
                title = cosp['title']
                bill_state_id = data['bill_id']
                politician_id = cosp['bioguide_id']
                # link and add to database
                db.execute(
                    "INSERT INTO sponsorship(sponsor_type, bill_state_id, politician_id) VALUES (:sponsor_type, :bill_state_id, :politician_id)",
                    {"sponsor_type": sponsor_type, "bill_state_id": bill_state_id, "politician_id": politician_id}
                )

            db.commit()


#just making sure this works
if __name__ == "__main__":
    engine = create_engine('sqlite:///../political_db.db', echo=True)
    db = scoped_session(sessionmaker(bind=engine))

    relative_congress_loc = "../../congress/data/"

    meta = MetaData()

    sponsorship = Table(
        'sponsorship', meta,
        Column('id', Integer, primary_key=True),
        Column('sponsor_type', String),
        Column('bill_state_id', String),
        Column('politician_id', String),
        sqlite_autoincrement=True
    )

    meta.create_all(engine)
    insert_sponsors()
