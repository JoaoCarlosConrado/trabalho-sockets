from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException

class setSettings:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_min_max(message_json)
        self._verify_unit_of_measurement(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_min_max(message_json):
        try:
            message_json["min"] = float(message_json["min"])
            message_json["max"] = float(message_json["max"])
        except ValueError:
            raise CustomException("ERROR", "Min and Max must be numbers")
        
    @staticmethod
    def _verify_unit_of_measurement(message_json):
        if message_json["data_type"] == "temperature":
            if message_json["unit_of_measurement"] not in gv.TEMPERATUREUM:
                raise CustomException("ERROR", "Unit of measurement not supported")
        elif message_json["data_type"] == "humidity":
            if message_json["unit_of_measurement"] not in gv.HUMIDITYUM:
                raise CustomException("ERROR", "Unit of measurement not supported")
        elif message_json["data_type"] == "co2":
            if message_json["unit_of_measurement"] not in gv.CO2LEVELUM:
                raise CustomException("ERROR", "Unit of measurement not supported")
        
        
    @staticmethod
    def execute(message_json):
        if message_json["data_type"] == "temperature":
            gv.TEMPERATUREMIN = message_json["min"]
            gv.TEMPERATUREMAX = message_json["max"]
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings set", message_json["data_type"], gv.TEMPERATUREMIN, gv.TEMPERATUREMAX, gv.TEMPERATUREUM)
        elif message_json["data_type"] == "humidity":
            gv.HUMIDITYMIN = message_json["min"]
            gv.HUMIDITYMAX = message_json["max"]
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings set", message_json["data_type"], gv.HUMIDITYMIN, gv.HUMIDITYMAX, gv.HUMIDITYUM)
        elif message_json["data_type"] == "co2":
            gv.CO2LEVELMIN = message_json["min"]
            gv.CO2LEVELMAX = message_json["max"]
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings set", message_json["data_type"], gv.CO2LEVELMIN, gv.CO2LEVELMAX, gv.CO2LEVELUM)
        return response