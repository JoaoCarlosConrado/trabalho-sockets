from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException

class getValue:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_data_type(message_json)
        self._verify_unit_of_measurement(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_data_type(message_json):
        if message_json["data_type"] not in ["temperature", "humidity", "co2"]:
            raise CustomException("ERROR", "Data type not supported")
    
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
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value retrieved", message_json["data_type"], gv.TEMPERATURE, gv.TEMPERATUREUM)
        elif message_json["data_type"] == "humidity":
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value retrieved", message_json["data_type"], gv.HUMIDITY, gv.HUMIDITYUM)
        elif message_json["data_type"] == "co2":
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value retrieved", message_json["data_type"], gv.CO2LEVEL, gv.CO2LEVELUM)
        return response