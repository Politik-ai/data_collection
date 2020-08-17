#!/usr/bin/env python3
import yaml
import os
from datetime import date
from sqlalchemy import Table, Column, Integer, String, Date, func
from framework import Politician, Politician_Term, Leadership_Role


def add_legislators(session, existing_bioguides = []):

    current_yaml = 'congress-legislators/legislators-current.yaml'
    historical_yaml = 'congress-legislators/legislators-historical.yaml'
    congress_dir = '../../congress/'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, congress_dir + current_yaml)
    skips, pol_terms_added, pols_added = 0, 0, 0

    # open up the yaml files
    for y in [current_yaml, historical_yaml]:
        with open(congress_dir + y) as file:
            info = yaml.full_load(file)
            for item in info:

                #forms of ID used
                bioid = item['id']['bioguide']
                lis = item['id'].get('lis', None)
                thomas_id = item['id'].get('thomas', None)
                
                if bioid in existing_bioguides:
                    #skip over bioguide if it doesn't exist
                    continue

                gender = item['bio']['gender']
                dob = item['bio'].get('birthday', '0001-01-01')
                dob = date(*[int(i) for i in dob.split('-')])
                first_name = item['name']['first']
                last_name = item['name']['last']

                #skips if the politician is from a long time ago (arbitrary cutoff)
                if dob.year < 1900:
                    skips += 1
                    continue

                new_pol = Politician(bioid, thomas_id, dob, first_name, last_name, lis)
                session.add(new_pol)
                pols_added += 1
                pol_id = session.query(Politician.id).filter(Politician.bioid == bioid).first()[0]

                #Adding Politician Terms
                for term in item['terms']:

                    start_date = date(*[int(i) for i in term['start'].split('-')])
                    end_date = date(*[int(i) for i in term['end'].split('-')])
                    #arbitrary cutoff for old terms
                    if end_date.year < 1950:
                        continue

                    party = term.get('party', "NA")
                    body = term['type']
                    state = term['state']
                    if body == 'rep':
                        district = term['district']
                    else:
                        district = None
                    
                    pol_term = Politician_Term(pol_id, start_date, end_date, party, \
                        state, body, gender, district)
                    session.add(pol_term)            
                    pol_terms_added += 1

                #Adding leadership roles
                if 'leadership_roles' in item:
                    for role in item['leadership_roles']:
                        start = date(*[int(i) for i in role['start'].split('-')])
                        end = date(*[int(i) for i in role['end'].split('-')]) if 'end' in role else None

                        leader_role = Leadership_Role(role['title'], role['chamber'], start, end, pol_id)
                        session.add(leader_role)

    session.commit()
    print(f"{pols_added} Politician added")
    print(f"{pol_terms_added} Politician_Terms added")
