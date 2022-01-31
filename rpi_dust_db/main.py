import time
import datetime
import board
import busio
import serial
from sds_reader import sds_reader
from rdsDB import database_handler
from gpiozero import LED, Button



import bme680
import time
import csv 




try:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)


sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

ledGR = LED(5)
ledRED = LED(27)
button = Button(26)

#Pobieranie aktualnego czasu i odmierzanie do gotowosci odczytania poprawnie IAQ. 
# Czas burn_in_time odczytany z dokumentacji czujnika BME680 nie powinien byc mniejszy niz 300 sekund aby pomiar byl dokladny
# burn_in_time -> czas do poprawnego przeliczenia i  odczytu IAQ  


start_time = time.time()
curr_time = time.time()
burn_in_time = 10
burn_in_data = []
id_measurement = 1
to_continue = True
drondb = database_handler()
ledRED.on()



if __name__=="__main__":
    while to_continue:
        if button.is_pressed:
            ledGR.on()
            last_print = time.monotonic()
            sds = sds_reader()
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            timestampDB = timestamp.replace('-','_').replace(' ','_').replace(':','_')
            tb_name = "measurements" + str(timestampDB)
            tb_name = tb_name.replace('-','_')
            drondb.create_new_table_into_db(tb_name)

            
            try:
                print('Oczekiwanie 300 sekund na dane do okreslenia wspolczynnika jakosci powietrza\n')
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
                

                while to_continue:  
                    if button.is_pressed:  
                        ledRED.off()
                        ledGR.on()
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

                            current = time.monotonic()
                            
                            if current - last_print >= 1.0:
                                last_print = current
                                ledGR.off()
                                dust = sds.read_dust()
                                print("PM 10: {} μg/m3".format(dust[0]))
                                print("PM 2.5: {} μg/m3".format(dust[1])) 
                                print('Temperature : {0:.2f} C'.format(sensor.data.temperature))
                                print('Humidity : {0:.2f} %RH'.format(sensor.data.humidity))
                                print('IAQ : {0:.2f}'.format(air_quality_score))
                                print('Pressure : {0:.2f} hPa'.format(sensor.data.pressure))
                                print("-------------------------------------------------------------------------")
                                
                                #Zapis do bazy danych RDS isteniejącej na usługach chumorowych AWS  
                                drondb.insert_values_measurement(tb_name,id_measurement,dust[0],dust[1],sensor.data.humidity,sensor.data.pressure,sensor.data.temperature,air_quality_score,timestamp)
                                
                                #ins.insert_values_localization(tb_name,id_measurement,50.238424224,55.238424224,7)
                                id_measurement+=1
                                
                                # air_quality_score = round(air_quality_score, 2)
                                # dict = {'hour':gps.timestamp_utc.tm_hour,'min':gps.timestamp_utc.tm_min,'sec':gps.timestamp_utc.tm_sec,'PM10':data[0],'PM25':data[1],'IAQ':air_quality_score,'Cisn':sensor.data.pressure,'Temp':sensor.data.temperature}
                                # df = pd.DataFrame(dict,index=[0])
                                #saving
                                #df.to_csv('danetry.csv')
                                #df.to_csv('dane1.csv', header=None, mode='a')
                    else:
                        ledRED.on()
                        print("Włącz przycisk")

                    
            except KeyboardInterrupt:
                to_continue = False
                pass

        

        else:
            print("Włącz przycisk")