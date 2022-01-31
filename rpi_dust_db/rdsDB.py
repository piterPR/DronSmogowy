import pymysql
import json
import collections


class database_handler:
    def __init__(self):
        self.db = pymysql.connect(host='xxxxxxxxxxxxxxxxxxxxxxx',
                             user='root',
                             password='eFBlUqBF1pCbcignLJPd',
                             database='dron_smogowy',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             ssl_ca= 'xxxxxxxxxxxxxxx',
                             ssl_cert = 'xxxxxxxxxxxxxxxxxxxx',
                             ssl_key = 'xxxxxxxxxxxxxxxxxx')
 




    def insert_values_measurement(self,db_name,IdMeasurement,pm10,pm25,humidity,hPa,temperature,IAQ,time):
        mycursor = self.db.cursor()
        query = 'INSERT INTO dron_smogowy.{}(IdMeasurement,pm10,pm25,humidity,hPa,temperature,IAQ,time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'.format(db_name)
        val = (IdMeasurement,pm10,pm25,humidity,hPa,temperature,IAQ,time)
        mycursor.execute(query,val)
        self.db.commit()
        print(mycursor.rowcount, "record(s) inserted.")

    def insert_values_localization(self,tb_name,id,longtitude,latitude,satelite):
        mycursor = self.db.cursor()
        query = 'INSERT INTO dron_smogowy.{}(IdMeasurement, longitude, latitude) VALUES(%s, %s, %s)'.format(tb_name)
        val = (id,longtitude,latitude)
        mycursor.execute(query,val)
        self.db.commit()
        print(mycursor.rowcount, "record(s) inserted into localization.")



    def read_specific_value(self,chosen_value):
        mycursor = self.db.cursor()
        querry='SELECT {} dron_smogowy.measurement'.format(chosen_value)
        mycursor.execute(querry)
        rows = mycursor.fetchall()


    def create_new_table_into_db(self,name):
        mycursor = self.db.cursor()
        print(name)
        querry='CREATE TABLE {} (IdMeasurement INT AUTO_INCREMENT PRIMARY KEY, pm10 FLOAT, pm25 FLOAT, humidity FLOAT, hPa FLOAT, temperature FLOAT, IAQ FLOAT, time TIMESTAMP)'.format(name)
        print(querry)
        mycursor.execute(querry)



    def save_values_measurement_to_json_file(self,database_name):
        mycursor = self.db.cursor()
        query = 'SELECT * FROM dron_smogowy.{}'.format(database_name)
        mycursor.execute(query)
        rows = mycursor.fetchall()

        object_list = []
        for x in rows:
            print(x)
            d = collections.OrderedDict()
            d["pm10"] = x.get("pm10")
            d["pm25"] = x.get("pm25")
            d["humidity"] = x.get("humidity")
            d["hPa"] = x.get("hPa")
            d["temperature"] = x.get("temperature")
            d["IAQ"] = x.get("IAQ")
            d["time"] = x.get("time").strftime('%Y-%m-%d %H:%M:%S')
            object_list.append(d)




        result = {"measurements":object_list}
        j = json.dumps(result,indent=7)

        with open(self.path_json_file, "w") as f:
            f.write(j)





