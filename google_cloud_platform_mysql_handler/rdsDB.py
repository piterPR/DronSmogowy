import pymysql
import json
import collections


class database_handler:
    def __init__(self):
        self.db = pymysql.connect(host='X.X.X.X',
                             user='XXX',
                             password='XXXX',
                             database='XXXX',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             ssl_ca= 'XXX',
                             ssl_cert = 'XXX',
                             ssl_key = 'XXX')




    def insert_values_measurement(self,id,pm10,pm25,humidity,hPa,satelites,temperature,IAQ,time):
        mycursor = self.db.cursor()
        query = 'INSERT INTO dron_smogowy.measurement(IdMeasurement,pm10,pm25,humidity,hPa,temperature,IAQ,time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (id,pm10,pm25,humidity,hPa,temperature,IAQ,time)
        mycursor.execute(query,val)
        self.db.commit()
        print(mycursor.rowcount, "record(s) inserted.")


    def save_values_measurement_to_json_file(self):
        mycursor = self.db.cursor()
        query = 'SELECT * FROM dron_smogowy.measurement'
        mycursor.execute(query)
        rows = mycursor.fetchall()

        object_list = []
        object_list_2 = []
        for x in rows:
            print(x)
            d = collections.OrderedDict()
            d["pm10"] = x.get("pm10")
            d["pm25"] = x.get("pm25")
            d["humidity"] = x.get("humidity")
            d["hPa"] = x.get("hPa")
            d["temperature"] = x.get("temperature")
            d["IAQ"] = x.get("IAQ")
            # d["time"] = x.get("time")
            object_list.append(d)

        x = collections.OrderedDict()
        x['measurements'] = object_list
        object_list_2.append(x)
        j = json.dumps(object_list_2, indent=7)
        with open("student_objects.json", "w") as f:
            f.write(j)




