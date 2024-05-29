from time import sleep
from sdtp.sdtpClient import *
from greenhouse.changeFiles import changeFiles as cf
import ports as p

def execute():
    while True:
        try:
            temperatureid = cf.getID("temperature")
            message = SensorRequestConnection("chavepix", "temperature", f"{temperatureid}")
            response = send_request("127.0.0.1", p.TCPSERVERPORT, message)
            print(response)
            response = json.loads(response)
            if response["status"] == "OK":
                break
            
        except Exception as e:
            print(e)
        print("Trying again in 15 seconds")
        sleep(15)
    
    while True:
        try:
            temperature_str = cf.readFile("temperature")
            message = SensorRequestMessage("chavepix", "temperature", f"{temperatureid}", "CELSIUS", f"{temperature_str}")
            sleep(1)
            send_request("127.0.0.1", p.UDPSERVERPORT, message)
            print("Temperature level sent")
        except Exception as e:
            print(e)