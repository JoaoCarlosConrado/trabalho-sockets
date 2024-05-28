from time import sleep
from sdtpClient import *

TCPSERVERPORT = 65432        
UDPSERVERPORT = 65433      
TCPACTUATORPORT = 65434

def test_conn_sensor():
    message = SensorRequestConnection("chavepix", "temperature", "temperature1")
    response = send_request("127.0.0.1", TCPSERVERPORT, message)
    print(response)

def test_sensor():
    message = SensorRequestMessage("chavepix", "temperature", "temperature1", "CELSIUS", "25.0")
    response = send_request("127.0.0.1", UDPSERVERPORT, message)
    print(response)

def test_getSettings():
    message = SettingsRequestMessage("chavepix", "GET", "temperature", "0", "0", "CELSIUS")
    response = send_request("127.0.0.1", UDPSERVERPORT, message)
    print(response)

def test_setSettings():
    message = SettingsRequestMessage("chavepix", "SET", "temperature", "12", "17", "CELSIUS")
    response = send_request("127.0.0.1", UDPSERVERPORT, message)
    print(response)

def test_getValue():
    message = ValueRequestMessage("chavepix", "humidity", "PERCENTAGE")
    response = send_request("127.0.0.1", UDPSERVERPORT, message)
    print(response)

def test_actuator():
    message = ActuatorRequestConnection("chavepix", "heater", "heater1")
    response = send_request("127.0.0.1", TCPSERVERPORT, message)
    print(response)

def test_actuator_activate():
    message = ActuatorRequestMessage("chavepix", "ACTIVATE","heater", "heater-1")
    response = send_request("127.0.0.1", TCPACTUATORPORT, message)
    print(response)

def test_actuator_disable():
    message = ActuatorRequestMessage("chavepix", "DISABLE","heater", "heater-1")
    response = send_request("127.0.0.1", TCPACTUATORPORT, message)
    print(response)


test_actuator_activate()
sleep(8)
test_actuator_disable()