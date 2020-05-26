#currently not working
import sqlalchemy
import pandas as pd
import sys
#args are 1-username, 2-password, 3-server, and 3-database of server, 4-csv file

username = "root"
password = "guest"
server = "127.0.0.1"
database = "political_db"
csv = "pol_db.csv"

#MySQL database connection


engine_stmt = 'mysql+mysqldb://%s:%s@%s:3306/%s' % (username, password,
                                                    server,database)
engine = sqlalchemy.create_engine(engine_stmt)

# get your data into pandas
df = pd.read_csv(csv)

# write the entire dataframe to database
df.to_sql(name='politician_term', con=engine, if_exists='append', index=False, chunksize=1000)
print('All data inserted!')