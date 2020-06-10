
DB=political_db.db
if test -f "$DB"; then
    rm $DB
    echo "Removed old db"
fi

cd database_filler
./parse_legislators.py
echo "Added legislators"
./parse_bills.py
echo "Added bills"
./parse_sponsor.py
echo "Added Sponsors"
./parse_bill_ref.py
echo "Added Bill Refs"
./parse_topics.py
echo "Added Topics"
#./parse_votes.py
#echo "Added votes"
cd .. 