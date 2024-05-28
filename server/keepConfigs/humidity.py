import server.globalVars as gv
from sdtp import sdtpClient
import json

def keep_humidity():
    HOST = "127.0.0.1"
    TCPPORT = 65434
    try:
        if gv.HUMIDITY <= gv.HUMIDITYMIN + (1 / 100 * gv.HUMIDITYMIN):
            if gv.IRRIGATIONSYSTEMSTATUS == "DISABLED":  # Ativando o sistema de irrigação
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "ACTIVATE", "irrigationsystem", gv.IRRIGATIONSYSTEMID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.IRRIGATIONSYSTEMSTATUS = "ACTIVE"
                    print("Sistema de irrigação ativado")
                else:
                    print("Erro ao ativar o sistema de irrigação")
        elif gv.HUMIDITY >= gv.HUMIDITYMAX - (1 / 100 * gv.HUMIDITYMAX):
            if gv.IRRIGATIONSYSTEMSTATUS == "ACTIVE":  # Desativando o sistema de irrigação
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "DISABLE", "irrigationsystem", gv.IRRIGATIONSYSTEMID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.IRRIGATIONSYSTEMSTATUS = "DISABLED"
                    print("Sistema de irrigação desativado")
                else:
                    print("Erro ao desativar o sistema de irrigação")
    except Exception as e:
        print("Erro ao manter a humidade:", e)
