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




all_voting_dirs = get_all_vote_dirs()

for vote_dir in all_voting_dirs:
    with open(vote_dir + "/data.json"):
        