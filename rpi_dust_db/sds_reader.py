import serial
import time



class sds_reader:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0',baudrate=9600)

    def read_dust(self):
        
        data = []
        for index in range(0,10):
            datum = self.ser.read()
            data.append(datum)
        pmtwofive = int.from_bytes(b''.join(data[2:4]),byteorder='little')/10
        pmten = int.from_bytes(b''.join(data[4:6]),byteorder='little')/10
        time.sleep(1)
        # print(pmten)
        #print("PM 10: {} μg/m3".format(pmten))
        #print("PM 2.5: {} μg/m3".format(pmtwofive))

        return pmten,pmtwofive
