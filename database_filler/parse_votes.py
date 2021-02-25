#!/usr/bin/env python3
import json
from datetime import datetime
from base import Session, engine, Base
from framework import Bill, Vote, Vote_Politician, Bill_State, Politician


def add_votes(session, all_voting_dirs, existing_vote_info):

    relative_congress_loc = "../../congress/data/"
    answer_dict = {'Yea': 1, 'Aye': 1, 'Nay': 0, 'No': 0, 'Present': -2, 'Not Voting': -1}
    date_format = "%Y-%m-%dT%H:%M:%S"
    num_votes, num_pol_votes = 0, 0
    i, skips, total_len = 0, 0, len(all_voting_dirs)
    for vote_dir in all_voting_dirs:
        
        i += 1
        #print(f"{i}/{total_len}")
        with open(vote_dir + "/data.json") as f:
            data = json.load(f)
            if "bill" in data:

                bill_code = data["bill"]["type"] + str(data["bill"]["number"]) + "-" + str(data["bill"]["congress"])
                vote_name = data["vote_id"]
                vote_date = datetime.strptime(data['date'][:-6], date_format).date()
                
                if [bill_code, vote_date] in existing_vote_info:
                    print('skipping')
                    continue

                bill = session.query(Bill).filter(Bill.bill_code == bill_code).first()

                if not bill:
                    print(f'no bill code found in database: {bill_code}')
                    continue

                new_vote = Vote(bill_code, bill.id, vote_date)
                #print("Added vote!")

                num_votes += 1

                for vote_type in data["votes"]:
                    if vote_type in answer_dict:
                        for pol_vote in data["votes"][vote_type]:
                            #try:
                            num_pol_votes += 1

                            politician = session.query(Politician).filter(Politician.bioid == pol_vote["id"]).first()
                            if not politician:
                                politician = session.query(Politician).filter(Politician.lis == pol_vote['id']).first()
                                if not politician:
                                    print('failed to get polid from bioid or lis')
                                    continue
                            
                            vote_pol = Vote_Politician(new_vote.id,answer_dict[vote_type], politician.id)
                            vote_pol.politician = politician

                            new_vote.vote_politicians.append(vote_pol)
                            #print("Added vote pol!")
                            #except:
                            #    print('unknown pol_vote type, should be dict:')
                            #    print(pol_vote)
                    else:
                        print(f"Not supported vote type: {vote_type}")
                
                session.add(new_vote)
            else:
                #print('no bill id in vote data')
                continue

    print(f'{num_votes} Votes Added')
    print(f'{num_pol_votes} Politician Votes Added')
    session.commit()
    