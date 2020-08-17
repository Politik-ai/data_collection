
DB=political_db.db
if test -f "$DB"; then
    rm $DB
    echo "Removed old db"
fi

cd database_filler
./update.py