import time, json, datetime, board, busio, serial, bme680, requests, sys
from sds_reader import sds_reader
from pymavlink import mavutil
from pymavlink import mavutil

#import board
#import busio
#import serial

#import bme680
#import time



API_URL="http://test.com"
start_time = time.time()
curr_time = time.time()
burn_in_time = 10
burn_in_data = []

try:
    # BME680
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    # MAVLINK
    mavlink_data = mavutil.mavlink_connection('/dev/ttyACM0')
    mavlink_data.wait_heartbeat()


except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)


def read_mavlink(): 

    if(mavlink_data.target_system == 0):
        mavlink_data.wait_heartbeat()
    else:
        time.sleep(1)
        altitude = mavlink_data.messages['GPS_RAW_INT'].lat  # Note, you can access message fields as attributes!
        longtitude = mavlink_data.messages['GPS_RAW_INT'].lon 
        satelite = mavlink_data.messages['GPS_RAW_INT'].satellites_visible
        timestamp = mavlink_data.time_since('GPS_RAW_INT')
        print(longtitude)
        print(altitude)
        print(satelite)


def print_stdout_values(PM,MAVLINK):
    print("PM 10: {} μg/m3".format(PM[0]))
    print("PM 2.5: {} μg/m3".format(PM[1])) 
    print('Temperature : {0:.2f} C'.format(sensor.data.temperature))
    print('Humidity : {0:.2f} %RH'.format(sensor.data.humidity))
    print('IAQ : {0:.2f}'.format(air_quality_score))
    print('Pressure : {0:.2f} hPa'.format(sensor.data.pressure))
    print('Lng : {0:.2f}'.format())
    print('Lat : {0:.2f}'.format())
    print("-------------------------------------------------------------------------")
        

def send_json_value(PM,API_URL,GPS):
    dictionary = {
        "measurement": "dron_smogowy_1",
        "lng": GPS.lng,
        "lan": GPS.lan,
        "temperature": sensor.data.temperature,
        "humidity": sensor.data.humidity,
        "iaq": air_quality_score,
        "pressue": sensor.data.pressure,
        "pm10": PM[0],
        "pm25": PM[1]
    }

    ready_json = json.dumps(dictionary, indent=9)
    print(ready_json)

    # Wyslij request do API 
    # r = requests.post(API_URL, ready_json)
    # print(f"Status Code: {r.status_code}, Response: {r.json()}")


if __name__=="__main__":
    last_print = time.monotonic()
    sds = sds_reader()

    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            outputbm = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas),outputbm)
            #print(sensor.data.pressure)
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = 40.0
    hum_weighting = 0.25

    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        gas_offset = gas_baseline - gas

        hum = sensor.data.humidity
        hum_offset = hum - hum_baseline

        # Obliczanie wilgotnosci na podstawie dokumentacji.
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset)
            hum_score /= (100 - hum_baseline)
            hum_score *= (hum_weighting * 100)

        else:
            hum_score = (hum_baseline + hum_offset)
            hum_score /= hum_baseline
            hum_score *= (hum_weighting * 100)

        # Obliczanie gazu na podstawie dokumentacji.
        if gas_offset > 0:
            gas_score = (gas / gas_baseline)
            gas_score *= (100 - (hum_weighting * 100))

        else:
            gas_score = 100 - (hum_weighting * 100)

        # IAQ = air_quality_score
        air_quality_score = hum_score + gas_score
        time.sleep(1)


        # odczyt paramsów 
        try:
            while True:
                # PM = sds.read_dust()
                # GPS = read_mavlink()
                # print_stdout_values(PM)
                # send_json_value(PM, API_URL,GPS)
                read_mavlink()
        except KeyboardInterrupt:
            print('interrupted!')

