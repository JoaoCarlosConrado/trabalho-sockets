from time import sleep
from sdtp.sdtpClient import *
from greenhouse.changeFiles import changeFiles as cf
import ports as p

def execute():
    while True:
        try:
            humidityid = cf.getID("humidity")
            message = SensorRequestConnection("chavepix", "humidity", f"{humidityid}")
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
            humidity_str = cf.readFile("humidity")
            message = SensorRequestMessage("chavepix", "humidity", f"{humidityid}", "PERCENTAGE", f"{humidity_str}")
            sleep(1)
            send_request("127.0.0.1", p.UDPSERVERPORT, message)
            print("Humidity level sent")
        except Exception as e:
            print(e)