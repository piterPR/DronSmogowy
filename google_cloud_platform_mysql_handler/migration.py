import time
import datetime
from rdsDB import database_handler

drondb = database_handler()
drondb.save_values_measurement_to_json_file()



