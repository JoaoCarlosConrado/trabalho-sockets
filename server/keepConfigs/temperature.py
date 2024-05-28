import server.globalVars as gv
from sdtp import sdtpClient
import json

def keep_temperature():
    HOST = "127.0.0.1"
    TCPPORT = 65434
    try:
        if gv.TEMPERATURE <= gv.TEMPERATUREMIN + (1 / 100 * gv.TEMPERATUREMIN):
            if gv.HEATERSTATUS == "DISABLED":  # Deixar o aquecedor ligado
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "ACTIVATE", "heater", gv.HEATERID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.HEATERSTATUS = "ACTIVE"
                    print("Aquecedor ativado")
                else:
                    print("Erro ao ativar o aquecedor")
            elif gv.COOLERSTATUS == "ACTIVE":  # Deixar o refrigerador desligado
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "DISABLE", "cooler", gv.COOLERID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.COOLERSTATUS = "DISABLED"
                    print("Refrigerador desativado")
                else:
                    print("Erro ao desativar o refrigerador")
        elif gv.TEMPERATURE >= gv.TEMPERATUREMAX - (1 / 100 * gv.TEMPERATUREMAX):
            if gv.COOLERSTATUS == "DISABLED":  # Deixar o refrigerador ligado
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "ACTIVATE", "cooler", gv.COOLERID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.COOLERSTATUS = "ACTIVE"
                    print("Refrigerador ativado")
                else:
                    print("Erro ao ativar o refrigerador")
            elif gv.HEATERSTATUS == "ACTIVE":  # Deixar o aquecedor desligado
                message = sdtpClient.ActuatorRequestMessage(gv.KEY, "DISABLE", "heater", gv.HEATERID)
                response = sdtpClient.send_request(HOST, TCPPORT, message)
                print(response)
                response = json.loads(response)
                if response["status"] == "OK":
                    gv.HEATERSTATUS = "DISABLED"
                    print("Aquecedor desativado")
                else:
                    print("Erro ao desativar o aquecedor")
    except Exception as e:
        print("Erro ao manter a temperatura:", e)
