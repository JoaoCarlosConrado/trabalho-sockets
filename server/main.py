import socket
import threading
import json
import time
import server.globalVars as gv
from sdtp import sdtpClient
from server.CustomException import CustomException
from server.udp_messages.setSensor import setSensor
from server.tcp_messages.connSensor import connSensor
from server.udp_messages.setSettings import setSettings
from server.udp_messages.getSettings import getSettings
from server.udp_messages.getValue import getValue
from server.tcp_messages.connActuator import connActuator
from server.keepConfigs.temperature import keep_temperature
from server.keepConfigs.humidity import keep_humidity
from server.keepConfigs.co2 import keep_co2
# Função para lidar com as mensagens TCP
def handle_tcp_client(conn, addr):
    print('Conexão TCP estabelecida de:', addr)
    with conn:
        try:
            while True:
                # Recebe a mensagem do cliente TCP
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print('Mensagem recebida do cliente TCP', addr, ':', message)
                # Converte a mensagem para JSON
                message_json = json.loads(message)
                print('Mensagem JSON:', message_json)
                response = None

                # Lógica para processar a mensagem TCP
                if message_json["type"] == "CONN SENSOR":
                    connSensor.verify(connSensor, message_json)
                    response = connSensor.execute(message_json)
                elif message_json["type"] == "CONN ACTUATOR":
                    connActuator.verify(connActuator, message_json)
                    response = connActuator.execute(message_json)

                # Envia uma resposta de volta para o cliente TCP
                conn.sendall(str(response).encode())
                print('Resposta enviada para o cliente TCP', addr, ':', response)
        except CustomException as e:
            print("Erro ao processar mensagem TCP:", e)
            if message_json["type"] == "CONN SENSOR":
                response = sdtpClient.SensorResponseConnection(message_json["key"], e.getCode(), str(e), message_json["sensor_type"], None)
            elif message_json["type"] == "CONN ACTUATOR":
                response = sdtpClient.ActuatorResponseConnection(message_json["key"], e.getCode(), str(e), message_json["actuator_type"], None)
            conn.sendall(str(response).encode())

# Função para lidar com as mensagens UDP
def handle_udp_message(data, addr):
    try:
        print('Mensagem UDP recebida de:', addr)
        message_json = json.loads(data.decode())
        print('Mensagem JSON:', message_json)
        response = None
        
        # Lógica para processar a mensagem UDP
        if message_json["type"] == "SET SENSOR":
            setSensor.verify(setSensor, message_json)
            response = setSensor.execute(message_json)
        elif message_json["type"] == "SET SETTINGS":
            setSettings.verify(setSettings, message_json)
            response = setSettings.execute(message_json)
        elif message_json["type"] == "GET SETTINGS":
            getSettings.verify(getSettings, message_json)
            response = getSettings.execute(message_json)
        elif message_json["type"] == "GET VALUE":
            getValue.verify(getValue, message_json)
            response = getValue.execute(message_json)

        # Envia a resposta de volta para o cliente UDP
        if response:
            udp_server_socket.sendto(json.dumps(response.__dict__).encode(), addr)
            print('Resposta enviada para o cliente UDP', addr, ':', response)
    except CustomException as e:
        print("Erro ao processar mensagem UDP:", e)
        if message_json["type"] == "SET SENSOR":
            response = sdtpClient.ValueResponseMessage(message_json["key"], e.getCode(), str(e), message_json["sensor_type"], None, message_json["unit_of_measurement"])
        elif message_json["type"] == "SET SETTINGS":
            response = sdtpClient.SettingsResponseMessage(message_json["key"], e.getCode(), str(e), message_json["data_type"], None, None, None)
        elif message_json["type"] == "GET SETTINGS":
            response = sdtpClient.SettingsResponseMessage(message_json["key"], e.getCode(), str(e), message_json["data_type"], None, None, None)
        elif message_json["type"] == "GET VALUE":
            response = sdtpClient.ValueResponseMessage(message_json["key"], e.getCode(), str(e), message_json["data_type"], None, message_json["unit_of_measurement"])

        udp_server_socket.sendto(json.dumps(response.__dict__).encode(), addr)

# requisição tem um protocolo, verificadores e uma resposta

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
TCPPORT = 65432      # Porta para ouvir as conexões TCP
UDPPORT = 65433      # Porta para receber as mensagens UDP

# Cria um socket TCP/IP
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Associa o socket TCP ao endereço e porta especificados
tcp_server_socket.bind((HOST, TCPPORT))
# Define o servidor TCP para escutar conexões entrantes
tcp_server_socket.listen()

def socket_tcp():
    while True:
        print("Servidor TCP aguardando conexões...")
        # Aceita uma nova conexão TCP
        conn, addr = tcp_server_socket.accept()
        # Inicia uma nova thread para lidar com o cliente TCP
        tcp_client_thread = threading.Thread(target=handle_tcp_client, args=(conn, addr))
        tcp_client_thread.start()

# Cria um socket UDP/IP
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Associa o socket UDP ao endereço e porta especificados
udp_server_socket.bind((HOST, UDPPORT))
# Define o servidor UDP para receber mensagens

def socket_udp():
    while True:
        print("Servidor UDP aguardando mensagens...")
        # Recebe a mensagem UDP e o endereço do cliente
        data, addr = udp_server_socket.recvfrom(1024)
        # Inicia uma nova thread para lidar com a mensagem UDP
        udp_client_thread = threading.Thread(target=handle_udp_message, args=(data, addr))
        udp_client_thread.start()

# Inicia as threads para os sockets TCP e UDP
tcp_thread = threading.Thread(target=socket_tcp)
tcp_thread.start()
udp_thread = threading.Thread(target=socket_udp)
udp_thread.start()

# Manter medições dentro das configurações de temperatura, umidade e nível de CO2
def keep_measurements():
    time.sleep(5)
    while True:
        keep_temperature()
        keep_humidity()
        keep_co2()

# Inicia a thread para manter as medições
measurements_thread = threading.Thread(target=keep_measurements)
measurements_thread.start()

# Mantém o servidor em execução
while True:
    print(f"{type(gv.TEMPERATURE)}Temperatura: {gv.TEMPERATURE}")
    print(f"{type(gv.HUMIDITY)} Umidade: {gv.HUMIDITY}")
    print(f"{type(gv.CO2LEVEL)} Nível de CO2: {gv.CO2LEVEL}")
    print(f"Injetor de CO2: {gv.CO2INJECTORSTATUS}")
    print(f"Sistema de irrigação: {gv.IRRIGATIONSYSTEMSTATUS}")
    print(f"Aquecedor: {gv.HEATERSTATUS}")
    print(f"Resfriador: {gv.COOLERSTATUS}")
    time.sleep(1)
    pass