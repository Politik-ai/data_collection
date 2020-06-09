#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, exists
from sqlalchemy.orm import scoped_session, sessionmaker




def insert_topics():

    global num_topics
    num_topics = 0


    def add_topic_if_new(topic):
        global num_topics
        topic_dict = {}

        exist = session.query(exists().where(topics.c.topic_name==topic)).scalar()
        #print('finished query')
        #print(exist)

        if not exist:
            num_topics += 1
            print(f'adding new topic: {num_topics}')
            session.execute(
                "INSERT INTO topics(topic_name) VALUES (:topic_name)", {"topic_name": topic}
            )


    files = all_high_level_data_files()
    i = 0
    for f in files:
        i += 1
        print(f"File Number: {i}")
        path = relative_congress_loc + f + '/data.json'
        path = os.path.abspath(path)
        with open(path) as x:

            data = json.load(x)

            top_term = data['subjects_top_term']
            add_topic_if_new(top_term)

            bill_state_id = f[2] + f[3] + f[4] + '-' + f[1]

            for topic in data['subjects']:
                add_topic_if_new(topic)

                # link and add to database
                session.execute(
                    "INSERT INTO bill_topics(bill_state_id, topic_id) VALUES (:bill_state_id, :topic_id)",
                    {"bill_state_id": bill_state_id, "topic_id": topic}
                )

            session.commit()


#just making sure this works
if __name__ == "__main__":
    engine = create_engine('sqlite:///../political_db.db', echo=False)
    session = scoped_session(sessionmaker(bind=engine))

    relative_congress_loc = "../../congress/data/"

    meta = MetaData()

    topics = Table(
        'topics', meta,
        Column('id', Integer, primary_key=True),
        Column('topic_name', String),
        sqlite_autoincrement=True
    )

    bill_topics = Table(
        'bill_topics', meta,
        Column('id', Integer, primary_key=True),
        Column('bill_state_id', Integer),
        Column('topic_id', String),
        Column('top', Boolean),
        sqlite_autoincrement=True
    )

    meta.create_all(engine)
    insert_topics()