from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException

class connSensor:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_sensor_type(message_json)
        self._verify_sensor_id(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_sensor_type(message_json):
        if message_json["sensor_type"] not in ["temperature", "humidity", "co2"]:
            raise CustomException("ERROR", "Sensor type not supported")
    
    def _verify_sensor_id(message_json):
        if message_json["sensor_type"] == "temperature":
            if gv.TEMPERATUREID != None:
                raise CustomException("ERROR", "Temperature Sensor already connected")
        elif message_json["sensor_type"] == "humidity":
            if gv.HUMIDITYID != None:
                raise CustomException("ERROR", "Humidity Sensor already connected")
        elif message_json["sensor_type"] == "co2":
            if gv.CO2LEVELID != None:
                raise CustomException("ERROR", "CO2 Sensor already connected")

    @staticmethod
    def execute(message_json):
        if message_json["sensor_type"] == "temperature":
            gv.TEMPERATUREID = message_json["sensor_id"]
            response = sdtpClient.SensorResponseConnection(gv.KEY, "OK", "Sensor conectado com sucesso", "temperature", gv.TEMPERATUREID)
        elif message_json["sensor_type"] == "humidity":
            gv.HUMIDITYID = message_json["sensor_id"]
            response = sdtpClient.SensorResponseConnection(gv.KEY, "OK", "Sensor conectado com sucesso", "humidity", gv.HUMIDITYID)
        elif message_json["sensor_type"] == "co2":
            gv.CO2LEVELID = message_json["sensor_id"]
            response = sdtpClient.SensorResponseConnection(gv.KEY, "OK", "Sensor conectado com sucesso", "co2", gv.CO2LEVELID)
        return response