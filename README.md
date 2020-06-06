# data_collection

This is the high level repository for data collection. Several repositories collect data from different sources, and are then aggregated into a MySQL database here. 
'https://www.govtrack.us/files/archive/'

In order to create the database from all parsed json data from the 'UnitedStates/Congress' repository, just run the 'create_db.sh' script. Note, for this to work, the data must be collected from that repo first. This can be done using the setup scripts in the fullstack repo as well as by using contained 'congress' repos. 
