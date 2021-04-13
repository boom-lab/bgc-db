from sqlalchemy import create_engine
import datetime
import dotenv
import os
import pandas as pd

#Get environmental variables
dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DB_PASSWORD = os.environ['DB_PASSWORD']

engine = create_engine('postgresql://randerson:{}@ryan-postgresql.cwcqdrtjgldz.us-east-1.rds.amazonaws.com:5432/bgc-db'.format(DB_PASSWORD))        
t = {}
t['DATE_ADD'] = datetime.datetime.now()
t['FLOAT_WMO_id'] = '9999'
t['INTERNAL_ID'] = '9999'
t['TRANSMISSION_ID'] = '9999'
t['TRANSMISISON_TYPE'] = 'IRIDIUM'
t['INST_TYPE'] = '9999'
t['IRIDIUM_PROGRAM'] = '9999'
t['WMO_INST_TYPE'] = '9999'
t['WMO_RECORDER_TYPE'] = '9999'
t['START_TIME'] = datetime.datetime.now()
t['START_TIME_STATUS'] = 'estimated'
t['LAUNCH_TIME'] = datetime.datetime.now()
t['LAUNCH_TIME_STATUS'] = 'estimated'
t['LAUNCH_POSITION_LAT'] = 90
t['LAUNCH_POSITION_LON'] = -120
t['LAUNCH_POSITION_STATUS'] = 'estimated'
t['FIRST_DOWN_TIME_DELAY'] = '1 day'
t['CYCLE_TIME'] = '1 day'
t['DESCENT_TIME'] = '1 day'
t['NEUTRAL_DEPTH_TIME'] = '1 day'
t['ASCENT_TIME'] = '1 day'
t['SURFACE_TIME'] = '1 day'
t['TRANSMISSION_REPETITION_RATE'] = '1 day'
t['CLOCK_DRIFT'] = '1 day'
t['LAST_CYCLE'] = datetime.datetime.now()

profile_meta_df = pd.DataFrame(t, index=[0])

profile_meta_df.to_sql('metadata_float_metadata', engine, if_exists='append', index=False)