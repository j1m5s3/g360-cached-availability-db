# g360-cached-availability-db (Python 3.10.8)
    Install dependencies:
        pip install -r requirements.txt

## Contained in this repo are the following:
    * Mongo DB population scripts
    * Database server to query the database

## Mongo DB population scripts
    * `populate_db.py` - populates the database with the data from the csv files
        * To run, use the following command:
            * `python populate_db.py`
                * Ensure that there is a `data` folder in the same directory as the script that contains the csv files
                    * Export data from properties table and cached_live_availabilities table from desired environment

## Postgres psql commands to create .csv files
    * properties table
        * \copy (select  name, address1, guid, city_name, state_code, country_code, has_rooms_enabled from properties where has_rooms_enabled = true) to '/tmp/properties_has_rooms_enabled_1_19_2023.csv' with (format csv, header);
    * cached_live_availabilities table
        * \copy (select property_guid,response from cached_live_availabilities) to /tmp/cached_avail_1_19_2023.csv with (format csv, header);

## To run database server
    * sh run_db_server.sh
        * base url: http://localhost:8001
            * /availability/{start_date}/{end_date}
                * GET
                * start_date: YYYY-MM-DD
                * end_date: YYYY-MM-DD