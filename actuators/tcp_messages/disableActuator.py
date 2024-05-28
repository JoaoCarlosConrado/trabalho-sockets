from sdtp.sdtpClient import *
from server.CustomException import CustomException
from greenhouse.changeFiles import changeFiles as cf
import actuators.globalVars as gv

class disableActuator:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_actuator_type(message_json)
        self._verify_actuator_id(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")
    
    def _verify_actuator_type(message_json):
        if message_json["actuator_type"] not in ["heater", "cooler", "irrigationsystem", "co2injector"]:
            raise CustomException("ERROR", "Actuator type not supported")
        
    def _verify_actuator_id(message_json):
        if message_json["actuator_type"] == "heater":
            if message_json["actuator_id"] != cf.getID("heater"):
                raise CustomException("ERROR", "Heater wrong id")
        elif message_json["actuator_type"] == "cooler":
            if message_json["actuator_id"] != cf.getID("cooler"):
                raise CustomException("ERROR", "Cooler wrong id")
        elif message_json["actuator_type"] == "irrigationsystem":
            if message_json["actuator_id"] != cf.getID("irrigationsystem"):
                raise CustomException("ERROR", "Irrigation System wrong id")
        elif message_json["actuator_type"] == "co2injector":
            if message_json["actuator_id"] != cf.getID("co2injector"):
                raise CustomException("ERROR", "CO2 Injector wrong id")


    @staticmethod
    def execute(message_json):
        if message_json["actuator_type"] == "heater":
            cf.writeFile("heater", "DISABLED")
        elif message_json["actuator_type"] == "cooler":
            cf.writeFile("cooler", "DISABLED")
        elif message_json["actuator_type"] == "irrigationsystem":
            cf.writeFile("irrigationsystem", "DISABLED")
        elif message_json["actuator_type"] == "co2injector":
            cf.writeFile("co2injector", "DISABLED")
        response = ActuatorResponseConnection(message_json["key"], "OK", "Actuator disabled", message_json["actuator_type"], message_json["actuator_id"])
        return response