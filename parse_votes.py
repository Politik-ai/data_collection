#!/usr/bin/env python3

import sys
sys.path.insert(1, '../')
import json
import os, csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, exists
from sqlalchemy.orm import scoped_session, sessionmaker

from get_voting_answers import get_all_vote_dirs

answer_dict = {'Yea': 1, 'Aye': 1, 'Nay': 0, 'No': 0}

# How do I get bill state id for insertion of vote

# How do I access politician id from the politician table

# Sample column: 



def insert_votes():
    all_voting_dirs = get_all_vote_dirs()
    for vote_dir in all_voting_dirs:
        with open(vote_dir + "/data.json") as f:
            data = json.load(f)
            if "bill" in data:
                vote_id = data["vote_id"]

                vote_dict = dict()
                vote_dict["bill_state_id"] = data["bill"]["type"] + str(data["bill"]["number"]) + "-" + str(data["bill"]["congress"])
                vote_dict["vote_id"] = vote_id
                session.execute("INSERT INTO vote(vote_id, bill_state_id) VALUES (:vote_id, :bill_state_id)", vote_dict)
                
                for vote_type in data["votes"]:
                    for pol_vote in data["votes"][vote_type]:
                        if vote_type in answer_dict:
                            politician_vote_dict = dict()
                            politician_vote_dict["vote_id"] = vote_id
                            politician_vote_dict["response"] = answer_dict[vote_type]
                            politician_vote_dict["politician_id"] = pol_vote["id"]
                            session.execute("INSERT INTO vote_politician(vote_id, response, politician_id) VALUES (:vote_id, :response, :politician_id)", politician_vote_dict)

            

if __name__ == "__main__":
    print("got here")
    engine = create_engine('sqlite:///../political_db.db', echo=False)
    session = scoped_session(sessionmaker(bind=engine))
    relative_congress_loc = "../../congress/data/"

    meta = MetaData()

    vote = Table(
        'vote', meta,
        Column('id', Integer, primary_key=True),
        Column('vote_id', String),
        Column('bill_state_id', Integer),
        sqlite_autoincrement=True
    )

    vote_politician = Table(
        'vote_politician', meta,
        Column('id', Integer, primary_key=True),
        Column('vote_id', Integer),
        Column('politician_id', Integer),
        Column('response', Boolean),
        sqlite_autoincrement=True
    )

    meta.create_all(engine)
    insert_votes()
    session.commit()