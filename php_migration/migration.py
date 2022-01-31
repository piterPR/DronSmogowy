#!/usr/bin/env python
import time
import datetime
from rdsDB import database_handler
import sys





# Wykorzystanie do zapisu w rpi do nowej bazy danego dnia

# today = datetime.date.today()
# db_name = "measurements" + str(today)
# db_name = db_name.replace('-','_')
# print(db_name)
# drondb.create_new_table_into_db(db_name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        database_to_migrate = sys.argv[1]
    else:
        database_to_migrate = 'measurement'
    drondb = database_handler()
    print(database_to_migrate)
    drondb.save_values_measurement_to_json_file(database_to_migrate)


# TESTY

# to_contiune = True;
# ts = time.time()
# while(to_contiune):
#     for value in range(1,100):
#         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         drondb.insert_values_measurement(value,2,3,4,5,6,7,8,st)
#         time.sleep(1)
#
#     if (value == 99):
#         to_contiune = False