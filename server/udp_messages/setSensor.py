from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException
class setSensor:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_sensor_type(message_json)
        self._verify_sensor_id_and_unit(message_json)
        self._convert_value_to_float(message_json)
    
    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_sensor_type(message_json):
        if message_json["sensor_type"] not in ["temperature", "humidity", "co2"]:
            raise CustomException("ERROR", "Sensor type not supported")

    @staticmethod
    def _verify_sensor_id_and_unit(message_json):
        sensor_type = message_json["sensor_type"]
        sensor_id = message_json["sensor_id"]
        if sensor_type == "temperature":
            if sensor_id != gv.TEMPERATUREID:
                raise CustomException("ERROR", "Sensor ID not connected")
            if message_json["unit_of_measurement"] not in gv.TEMPERATUREUM:
                raise CustomException("ERROR", "Unit of measurement not supported")
        elif sensor_type == "humidity":
            if sensor_id != gv.HUMIDITYID:
                raise CustomException("ERROR", "Sensor ID not connected")
            if message_json["unit_of_measurement"] not in gv.HUMIDITYUM:
                raise CustomException("Unit of measurement not supported")
        elif sensor_type == "co2":
            if sensor_id != gv.CO2LEVELID:
                raise CustomException("ERROR", "Sensor ID not connected")
            if message_json["unit_of_measurement"] not in gv.CO2LEVELUM:
                raise CustomException("ERROR", "Unit of measurement not supported")

    @staticmethod
    def _convert_value_to_float(message_json):
        if message_json["sensor_type"] == "temperature":
            try:
                message_json["value"] = float(message_json["value"])
            except ValueError:
                raise CustomException("ERROR", "Value must be a number")
        elif message_json["sensor_type"] == "humidity":
            try:
                message_json["value"] = float(message_json["value"])
            except ValueError:
                raise CustomException("ERROR", "Value must be a number")
        elif message_json["sensor_type"] == "co2":
            try:
                message_json["value"] = float(message_json["value"])
            except ValueError:
                raise CustomException("ERROR", "Value must be a number")

    @staticmethod
    def execute(message_json):
        if message_json["sensor_type"] == "temperature":
            gv.TEMPERATURE = message_json["value"]
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value set", message_json["sensor_type"], gv.TEMPERATURE, message_json["unit_of_measurement"])
        elif message_json["sensor_type"] == "humidity":
            gv.HUMIDITY = message_json["value"]
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value set", message_json["sensor_type"], gv.HUMIDITY, message_json["unit_of_measurement"])
        elif message_json["sensor_type"] == "co2":
            gv.CO2LEVEL = message_json["value"]
            response = sdtpClient.ValueResponseMessage(gv.KEY, "OK", "Value set", message_json["sensor_type"], gv.CO2LEVEL, message_json["unit_of_measurement"])
        return response