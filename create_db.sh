pip3 install -r requirements.txt


DB=political_db.db
if test -f "$DB"; then
    rm $DB
    echo "Removed old db"
fi

cd database_filler
./parse_legislators.py
echo "Finished legislators"
./parse_bills.py
echo "Finished bills"
./parse_sponsor.py
echo "Finished Sponsors"
./parse_bill_ref.py
echo "Finished Bill Refs"
./parse_topics.py
echo "Finished Topics"
./parse_votes.py
echo "Finished votes"
cd .. 