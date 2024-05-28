from sdtp import sdtpClient
import server.globalVars as gv
from server.CustomException import CustomException

class connActuator:
    @staticmethod
    def verify(self, message_json):
        self._verify_key(message_json["key"])
        self._verify_actuator_type(message_json)
        self._verify_actuator_id(message_json)

    @staticmethod
    def _verify_key(key):
        if key != gv.KEY:
            raise CustomException("NOT AUTHORIZED", "Wrong key")

    @staticmethod
    def _verify_actuator_type(message_json):
        if message_json["actuator_type"] not in ["heater", "cooler", "irrigationsystem", "co2injector"]:
            raise CustomException("ERROR", "Actuator type not supported")

    @staticmethod
    def _verify_actuator_id(message_json):
        if message_json["actuator_type"] == "heater":
            if gv.HEATERID != None:
                raise CustomException("ERROR", "Heater already connected")
        elif message_json["actuator_type"] == "cooler":
            if gv.COOLERID != None:
                raise CustomException("ERROR", "Cooler already connected")
        elif message_json["actuator_type"] == "irrigationsystem":
            if gv.IRRIGATIONSYSTEMID != None:
                raise CustomException("ERROR", "Irrigation System already connected")
        elif message_json["actuator_type"] == "co2injector":
            if gv.CO2INJECTORID != None:
                raise CustomException("ERROR", "CO2 Injector already connected")

    @staticmethod
    def execute(message_json):
        if message_json["actuator_type"] == "heater":
            gv.HEATERID = message_json["actuator_id"]
            response = sdtpClient.ActuatorResponseConnection(gv.KEY, "OK", "Actuator connected successfully", "heater", gv.HEATERID)
        elif message_json["actuator_type"] == "cooler":
            gv.COOLERID = message_json["actuator_id"]
            response = sdtpClient.ActuatorResponseConnection(gv.KEY, "OK", "Actuator connected successfully", "cooler", gv.COOLERID)
        elif message_json["actuator_type"] == "irrigationsystem":
            gv.IRRIGATIONSYSTEMID = message_json["actuator_id"]
            response = sdtpClient.ActuatorResponseConnection(gv.KEY, "OK", "Actuator connected successfully", "irrigationsystem", gv.IRRIGATIONSYSTEMID)
        elif message_json["actuator_type"] == "co2injector":
            gv.CO2INJECTORID = message_json["actuator_id"]
            response = sdtpClient.ActuatorResponseConnection(gv.KEY, "OK", "Actuator connected successfully", "co2injector", gv.CO2INJECTORID)
        return response