import requests


class request:
    #def __init__(self):
       # self.request = (host='xxxxxxxxxxxxxxxxxxxxxxx')
 

    def save_values_measurement_to_json_file(self,measurement):
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

#       r = requests.post('http://httpbin.org/post', json={"key": "value"})
