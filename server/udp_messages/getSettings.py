from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException

class getSettings:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_data_type(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_data_type(message_json):
        if message_json["data_type"] not in ["temperature", "humidity", "co2"]:
            raise CustomException("ERROR", "Data type not supported")

    @staticmethod
    def execute(message_json):
        if message_json["data_type"] == "temperature":
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings retrieved", message_json["data_type"], gv.TEMPERATUREMIN, gv.TEMPERATUREMAX, gv.TEMPERATUREUM)
        elif message_json["data_type"] == "humidity":
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings retrieved", message_json["data_type"], gv.HUMIDITYMIN, gv.HUMIDITYMAX, gv.HUMIDITYUM)
        elif message_json["data_type"] == "co2":
            response = sdtpClient.SettingsResponseMessage(gv.KEY, "OK", "Settings retrieved", message_json["data_type"], gv.CO2LEVELMIN, gv.CO2LEVELMAX, gv.CO2LEVELUM)
        return response