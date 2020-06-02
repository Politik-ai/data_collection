from get_files_to_parse_v2 import get_all_paths
import json

import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    files = get_all_paths()

    for f in files:
        path = f[3]
        with open(path) as x:
            data = json.load(x)
            sponsor_type = data['sponsor']['type']
            state = data['sponsor']['state']
            title = data['sponsor']['title']
            bill_state_id = data['bill_id']
            politician_id = data['sponsor']['bioguide_id']
            # link and add to database
            db.execute(
                "INSERT INTO sponsor(sponsor_type, bill_state_id, politician_id) VALUES (:sponsor_type, :bill_state_id, :politician_id)",
                {"sponsor_type": sponsor_type, "bill_state_id": bill_state_id, "politician_id": politician_id}
            )
            db.commit()


#just making sure this works
if __name__ == "__main__":
    main()
