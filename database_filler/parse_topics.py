#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
from get_all_data_files import all_high_level_data_files
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, exists, select
from sqlalchemy.orm import scoped_session, sessionmaker

from base import Session, engine, Base
from framework import Bill, Topic, Bill_Topic

Base.metadata.create_all(engine)
session  = Session()
relative_congress_loc = "../../congress/data/"

def add_topic_if_new(topic):
    topic_dict = {}
    exist = session.query(Topic).filter(Topic.name == topic).first()

    if not exist:
        new_topic = Topic(topic)
        session.add(new_topic)

files = all_high_level_data_files()
i = 0
for f in files:
    i += 1
    path = relative_congress_loc + f + '/data.json'
    path = os.path.abspath(path)
    with open(path) as x:

        data = json.load(x)

        top_term = data['subjects_top_term']
        add_topic_if_new(top_term)
        parts = f.split('/')
        bill_code = parts[3] + '-' + parts[0]
        bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()

        for t_name in data['subjects']:
            add_topic_if_new(t_name)
            topic_id = session.query(Topic).filter(Topic.name == t_name).first().id
            new_bill_topic = Bill_Topic(bill.id,topic_id)
            session.add(new_bill_topic)

session.commit()

