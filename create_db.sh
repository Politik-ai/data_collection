rm political_db.db
cd database_filler
./parse_legislators.py
./parse_bills.py
./parse_sponsor.py
./parse_bill_ref.py
./parse_topics.py
#./parse_votes.py
cd .. 