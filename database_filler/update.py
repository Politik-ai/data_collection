#!/usr/bin/env python3
import sys, os
from base import Session, Base, engine
from framework import Bill, Topic, Bill_Topic, Politician, Bill_State, Vote
from get_bill_states_to_parse import get_bill_state_paths
from get_all_data_files import all_high_level_data_files
from get_voting_answers import get_all_vote_dirs


session = Session()

#Get existing Politicians in DB
if os.path.exists("../political_db.db"):
    #sys.path.append("../../political_analytics/")
    #from political_queries import *


    bills = session.query(Bill)
    existing_bill_codes = [b.bill_code for b in bills]

    topics = session.query(Topic)
    existing_topics = [t.name for t in topics]
    
    pols = session.query(Politician)
    existing_bioguides = [p.bioid for p in pols]

    billstates = session.query(Bill_State)
    existing_bill_state_identifiers = [b.bill_state_identifier for b in billstates]


    votes = session.query(Vote)
    existing_vote_info = [[v.bill_code, v.vote_date] for v in votes]

else:
    Base.metadata.create_all(engine)
    existing_bill_state_identifiers = []
    existing_bill_codes = []
    existing_topics = []
    existing_bioguides = []
    existing_vote_info = []


bs_paths = get_bill_state_paths()
bill_paths = all_high_level_data_files()
all_voting_dirs = get_all_vote_dirs()

from parse_legislators import add_legislators
add_legislators(session, existing_bioguides)

from parse_bills import add_bills_and_bill_states
add_bills_and_bill_states(session, bs_paths, existing_bill_codes, existing_bill_state_identifiers)

from parse_sponsor import add_sponsors
add_sponsors(session, bill_paths, existing_bill_codes)

from parse_bill_ref import add_bill_refs
add_bill_refs(session, bill_paths, existing_bill_codes)

from parse_topics import add_topics
add_topics(session, bill_paths, existing_bill_codes, existing_topics)

from parse_votes import add_votes
add_votes(session, all_voting_dirs, existing_vote_info)