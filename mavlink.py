import sys
import time
from pymavlink import mavutil
from pymavlink import mavutil

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('/dev/ttyACM0')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link

to_continue = True
while(to_continue):
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    if(the_connection.target_system == 0):
        the_connection.wait_heartbeat()
    else:
        time.sleep(1)
        altitude = the_connection.messages['GPS_RAW_INT'].lat  # Note, you can access message fields as attributes!
        longtitude = the_connection.messages['GPS_RAW_INT'].lon 
        satelite = the_connection.messages['GPS_RAW_INT'].satellites_visible
        timestamp = the_connection.time_since('GPS_RAW_INT')
        print(longtitude)
        print(altitude)
        print(satelite)

