import socket
import threading
import json
import time
from actuators.connectActuator import connActuator
from sdtp.sdtpClient import *
from server.CustomException import CustomException
from actuators.tcp_messages.activateActuator import activateActuator
from actuators.tcp_messages.disableActuator import disableActuator

# requisição tem um protocolo, verificadores e uma resposta
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
                if message_json["type"] == "ACTIVATE ACTUATOR":
                    activateActuator.verify(activateActuator, message_json)
                    response = activateActuator.execute(message_json)
                elif message_json["type"] == "DISABLE ACTUATOR":
                    disableActuator.verify(disableActuator, message_json)
                    response = disableActuator.execute(message_json)
                
                # Envia uma resposta de volta para o cliente TCP
                conn.sendall(str(response).encode())
                print('Resposta enviada para o cliente TCP', addr, ':', response)
        except CustomException as e:
            print("Erro ao processar mensagem TCP:", e)
            if message_json["type"] == "ACTIVATE ACTUATOR":
                response = ActuatorRequestConnection(message_json["key"], "ERROR", e.message)
            elif message_json["type"] == "DISABLE ACTUATOR":
                response = ActuatorRequestConnection(message_json["key"], "ERROR", e.message)
            conn.sendall(str(response).encode())
            

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
TCPPORT = 65434      # Porta para ouvir as conexões TCP

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

# Inicia as threads para os sockets TCP e UDP
tcp_thread = threading.Thread(target=socket_tcp)
tcp_thread.start()

#conectar atuadores

connActuator("heater")
connActuator("cooler")
connActuator("irrigationsystem")
connActuator("co2injector")

# Mantém o servidor em execução
while True:
    time.sleep(1)
    pass