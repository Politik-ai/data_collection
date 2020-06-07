cd database_filler
./parse_legislators.py
echo "Finished Legislators"
./parse_bills.py
echo "Finished Bills"
./parse_sponsor.py
echo "Finished Sponsors"
./parse_bill_ref.py
echo "Finished Bill references"
#./parse_topics.py
#./parse_votes.py
cd ..