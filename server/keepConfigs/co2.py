import json
import server.globalVars as gv
from sdtp import sdtpClient

def keep_co2():
    HOST = "127.0.0.1"
    TCPPORT = 65434

    if gv.CO2LEVELID is None:
        print("Sensor de CO2 não está conectado")
        return

    if gv.CO2INJECTORID is None:
        print("Injetor de CO2 não está conectado")
        return
    try:
        if gv.CO2LEVEL <= gv.CO2LEVELMIN + (1/100 * gv.CO2LEVELMIN):
            if gv.CO2INJECTORSTATUS == "DISABLED": # Ativando o injetor de CO2
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "ACTIVATE", "co2injector", gv.CO2INJECTORID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.CO2INJECTORSTATUS = "ACTIVE"
                    print("Injetor de CO2 ativado")
                else:
                    print("Erro ao ativar o injetor de CO2")
        elif gv.CO2LEVEL >= gv.CO2LEVELMAX - (1/100 * gv.CO2LEVELMAX):
            if gv.CO2INJECTORSTATUS == "ACTIVE": # Desativando o injetor de CO2
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "DISABLE", "co2injector", gv.CO2INJECTORID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.CO2INJECTORSTATUS = "DISABLED"
                    print("Injetor de CO2 desativado")
                else:
                    print("Erro ao desativar o injetor de CO2")
    except Exception as e:
        print("Erro ao manter a humidade:", e)