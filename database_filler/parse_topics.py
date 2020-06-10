#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, exists, select
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
            #print(f'adding new topic: {num_topics}')
            session.execute(
                "INSERT INTO topics(topic_name) VALUES (:topic_name)", {"topic_name": topic}
            )


    files = all_high_level_data_files()
    i = 0
    for f in files:
        i += 1
        #print(f"File Number: {i}")
        path = relative_congress_loc + f + '/data.json'
        path = os.path.abspath(path)
        with open(path) as x:

            data = json.load(x)

            top_term = data['subjects_top_term']
            add_topic_if_new(top_term)
            parts = f.split('/')
            #print(f)
            bill_id = parts[3] + '-' + parts[0]
            #print(bill_id)

            for topic in data['subjects']:
                add_topic_if_new(topic)
                #print(topic)
                print('query:')
                topics = session.query(topics).all()
                #topic_id = session.execute("SELECT * FROM topics WHERE topic_name = topic_name VALUES (:topic_name)",
                 #d{"topic_name": topic})
                topic_id = 1

                # link and add to database
                session.execute(
                    "INSERT INTO bill_topics(bill_id, topic_id) VALUES (:bill_id, :topic_id)",
                    {"bill_id": bill_id, "topic_id": topic_id}
                )

            session.commit()


#just making sure this works
if __name__ == "__main__":
    engine = create_engine('sqlite:///../political_db.db', echo=False)
    session = sessionmaker(bind=engine)()

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
        Column('bill_id', Integer),
        Column('topic_id', String),
        Column('top', Boolean),
        sqlite_autoincrement=True
    )

    meta.create_all(engine)
    insert_topics()
