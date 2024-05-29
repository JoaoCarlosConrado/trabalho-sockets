from time import sleep
from sdtp.sdtpClient import *
from greenhouse.changeFiles import changeFiles as cf
import ports as p

def execute():
    while True:
        try:
            co2id = cf.getID("co2level")
            message = SensorRequestConnection("chavepix", "co2", f"{co2id}")
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
            co2_str = cf.readFile("co2level")
            message = SensorRequestMessage("chavepix", "co2", f"{co2id}", "PPM", f"{co2_str}")
            sleep(1)
            send_request("127.0.0.1", p.UDPSERVERPORT, message)
            print("CO2 level sent")
        except Exception as e:
            print(e)