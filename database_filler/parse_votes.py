#!/usr/bin/env python3

import json
from datetime import datetime
from get_voting_answers import get_all_vote_dirs
from base import Session, engine, Base
from framework import Bill, Vote, Vote_Politician, Bill_State, Politician

session = Session()
relative_congress_loc = "../../congress/data/"
Base.metadata.create_all(engine)

answer_dict = {'Yea': 1, 'Aye': 1, 'Nay': 0, 'No': 0, 'Present': -2, 'Not Voting': -1}
date_format = "%Y-%m-%dT%H:%M:%S"

all_voting_dirs = get_all_vote_dirs()
num_votes, num_pol_votes = 0, 0
i, skips, total_len = 0, 0, len(all_voting_dirs)
for vote_dir in all_voting_dirs:
    
    i += 1
    print(f"{i}/{total_len}")
    with open(vote_dir + "/data.json") as f:
        data = json.load(f)
        if "bill" in data:

            #print('bill_id_found')
            bill_code = data["bill"]["type"] + str(data["bill"]["number"]) + "-" + str(data["bill"]["congress"])
            vote_name = data["vote_id"]
            bill_id = session.query(Bill.id).filter(Bill.bill_code == bill_code).first()

            if not bill_id:
                print(f'no bill code found in database: {bill_code}')
                continue
            
            bill_id = bill_id[0]
            matching_bill_states = session.query(Bill_State).filter(Bill_State.bill_id == bill_id).all()
            vote_date = datetime.strptime(data['date'][:-6], date_format).date()
            if not matching_bill_states:
                print('skipping, no matching bill_states found!')
                continue
            
            #NOTE: If there are no matching bill_states, what to do? For not skip, but better long term action?
            """
            Select all bill_states that match bill_id and
            Sort that selection by DateDiff from Vote Date and
            Select smallest positive diff as correct Bill_state.
            """
            date_diffs = [[bill_state.intro_date-vote_date, bill_state.id] for bill_state in matching_bill_states]
            bill_state_id = min(date_diffs, key = lambda t: t[0])[1]

            session.add(Vote(bill_state_id, vote_date))
            num_votes += 1
            vote_id = session.query(Vote).filter(Vote.bill_state_id == bill_state_id).first().id

            for vote_type in data["votes"]:
                if vote_type in answer_dict:
                    for pol_vote in data["votes"][vote_type]:
                        try:
                            num_pol_votes += 1

                            polid = session.query(Politician).filter(Politician.bioid == pol_vote["id"]).first()
                            if not polid:
                                polid = session.query(Politician).filter(Politician.lis == pol_vote['id']).first()
                                if not polid:
                                    print('failed to get polid from bioid or lis')
                                    continue
                            
                            session.add(Vote_Politician(vote_id,polid.id,answer_dict[vote_type]))
                        except:
                            print('unknown pol_vote type, should be dict:')
                            print(pol_vote)
                else:
                    print(f"Not supported vote type: {vote_type}")
        else:
            #print('no bill id in vote data')
            continue

print(f'{num_votes} Votes Added')
print(f'{num_pol_votes} Politician Votes Added')
session.commit()