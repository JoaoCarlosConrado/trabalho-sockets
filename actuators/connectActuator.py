import time
from sdtp.sdtpClient import *
import actuators.globalVars as gv
from greenhouse.changeFiles import changeFiles as cf

def connActuator(name):
    while True:
        try:
            response = send_request("127.0.0.1", 65432, ActuatorRequestConnection(gv.KEY, f"{name}", cf.getID(f"{name}")))
            print(response)
            response = json.loads(response)
            if response["status"] == "OK":
                break
        except Exception as e:
            print("Erro ao conectar com o servidor SDTP:", e)
        print("Tentando novamente em 15 segundos...")
        time.sleep(15)