import pymysql
import json
import collections


class database_handler:
    def __init__(self):
        self.db = pymysql.connect(host='35.187.87.235',
                             user='root',
                             password='eFBlUqBF1pCbcignLJPd',
                             database='dron_smogowy',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             ssl_ca= 'C:/Users/Admin/PycharmProjects/DronSmogowy/server-ca.pem',
                             ssl_cert = 'C:/Users/Admin/PycharmProjects/DronSmogowy/client-cert.pem',
                             ssl_key = 'C:/Users/Admin/PycharmProjects/DronSmogowy/client-key.pem')
        self.path_json_file = 'C:/Users/Admin/PycharmProjects/DronSmogowy/DronSmogowyAppAngular/src/app/main/chart/chart_data2.json'




    def insert_values_measurement(self,id,pm10,pm25,humidity,hPa,satelites,temperature,IAQ,time):
        mycursor = self.db.cursor()
        query = 'INSERT INTO dron_smogowy.measurements2022_01_02(IdMeasurement,pm10,pm25,humidity,hPa,temperature,IAQ,time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (id,pm10,pm25,humidity,hPa,temperature,IAQ,time)
        mycursor.execute(query,val)
        self.db.commit()
        print(mycursor.rowcount, "record(s) inserted.")



    def read_specific_value(self,chosen_value):
        mycursor = self.db.cursor()
        querry='SELECT {} dron_smogowy.measurement'.format(chosen_value)
        mycursor.execute(querry)
        rows = mycursor.fetchall()


    def create_new_table_into_db(self,name):
        mycursor = self.db.cursor()
        print(name)
        querry='CREATE TABLE {} (IdMeasurement INT, pm10 FLOAT, pm25 FLOAT, humidity FLOAT, hPa FLOAT, temperature FLOAT, IAQ FLOAT, time TIMESTAMP, measurementcol VARCHAR(50))'.format(name)
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





