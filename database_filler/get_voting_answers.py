#!/usr/bin/env python3
import json
import os

congress_data_dir = "../../congress/data"

def get_all_vote_dirs():
    all_vote_dirs = []
    for congress in os.listdir(congress_data_dir):
        votes_dir = congress_data_dir + "/" + congress + "/votes"
        for session in os.listdir(votes_dir):
            session_dir = votes_dir + "/" + session
            for vote in os.listdir(session_dir):
                all_vote_dirs.append(session_dir + "/" + vote)
    return all_vote_dirs

def get_vote_entries():
    entries = set()
    all_vote_dirs = get_all_vote_dirs()
    for vote_dir in all_vote_dirs:
        with open(vote_dir + "/data.json") as f:
            data = json.load(f)
            if "votes" in data:
                votes = data["votes"]
                [entries.add(vote) for vote in votes if vote not in entries]
    return entries