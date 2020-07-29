#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, exists, select
from sqlalchemy.orm import scoped_session, sessionmaker

from base import Session, engine, Base
from framework import Bill, Topic, Bill_Topic


def add_topics(session, files, existing_bill_codes, existing_topics):

    relative_congress_loc = "../../congress/data/"
    num_topics, num_bill_topics = 0, 0

    def add_topic_if_new(topic):
        if topic not in existing_topics:
            new_topic = Topic(topic)
            session.add(new_topic)
            nonlocal num_topics
            num_topics += 1
            existing_topics.append(topic)

    i = 0
    num_total_files = len(files)
    skips = 0
    for f in files:
        i += 1
        print(f"{i}/{num_total_files}")
        path = relative_congress_loc + f + '/data.json'
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            print('invalid path')
            continue
        with open(path) as x:

            data = json.load(x)
            top_term = data['subjects_top_term']
            add_topic_if_new(top_term)
            bill_code = data['bill_id']
            if bill_code in existing_bill_codes:
                print('skipping')
                continue

            bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()
            if not bill:
                print(f'skipping bill {bill_code}')
                skips +=1
                continue
            for t_name in data['subjects']:
                #print('adding bill')
                add_topic_if_new(t_name)
                topic_id = session.query(Topic).filter(Topic.name == t_name).first().id
                new_bill_topic = Bill_Topic(bill.id,topic_id)
                session.add(new_bill_topic)
                num_bill_topics += 1
    print(f"{skips} Bills skipped")
    print(f"{num_topics} Topics Added")
    print(f"{num_bill_topics} Bill Topics Added")
    session.commit()

if __name__ == "__main__":


    from get_all_data_files import all_high_level_data_files
    session = Session()
    bill_paths = all_high_level_data_files()

    add_topics(session, bill_paths, [], [])
