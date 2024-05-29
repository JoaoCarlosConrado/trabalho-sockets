import socket
import json
import logging
from sdtp.logger import setup_logging

# Configuração do logger
logger = setup_logging()

class Message:
    def __init__(self, type_, key):
        self.type = type_
        self.key = key

    def __str__(self):
        return json.dumps(self.__dict__)

# Conectar sensor ao servidor
class SensorRequestConnection(Message):
    def __init__(self, key, sensor_type, sensor_id):
        super().__init__("CONN SENSOR", key)
        self.sensor_type = sensor_type
        self.sensor_id = sensor_id
        self.protocol = socket.SOCK_STREAM

# Resposta da conexão do sensor ao servidor
class SensorResponseConnection(Message):
    def __init__(self, key, status, message, sensor_type, sensor_id):
        super().__init__("CONFIRM SENSOR", key)
        self.status = status
        self.message = message
        self.sensor_type = sensor_type
        self.sensor_id = sensor_id

# Requisição para sensor enviar valor obtido
class SensorRequestMessage(Message):
    def __init__(self, key, sensor_type, sensor_id, unit_of_measurement, value):
        super().__init__("SET SENSOR", key)
        self.sensor_type = sensor_type
        self.sensor_id = sensor_id
        self.unit_of_measurement = unit_of_measurement
        self.value = value
        self.protocol = socket.SOCK_DGRAM

# Conectar atuador ao servidor
class ActuatorRequestConnection(Message):
    def __init__(self, key, actuator_type, actuator_id):
        super().__init__("CONN ACTUATOR", key)
        self.actuator_type = actuator_type
        self.actuator_id = actuator_id
        self.protocol = socket.SOCK_STREAM

# Resposta da conexão do atuador ao servidor
class ActuatorResponseConnection(Message):
    def __init__(self, key, status, message, actuator_type, actuator_id):
        super().__init__("CONFIRM ACTUATOR", key)
        self.status = status
        self.message = message
        self.actuator_type = actuator_type
        self.actuator_id = actuator_id

# Ligar ou Desligar Atuador 
class ActuatorRequestMessage(Message):
    def __init__(self, key, action, actuator_type, actuator_id):
        if action == "ACTIVATE":
            super().__init__("ACTIVATE ACTUATOR", key)
        elif action == "DISABLE":
            super().__init__("DISABLE ACTUATOR", key)
        self.action = action
        self.actuator_type = actuator_type
        self.actuator_id = actuator_id
        self.protocol = socket.SOCK_STREAM

# Resposta ao requisitar que ligue ou desligue atuador
class ActuatorResponseMessage(Message):
    def __init__(self, key, status, message, actuator_type, actuator_id):
        super().__init__("RESPONSE ACTUATOR", key)
        self.status = status
        self.message = message
        self.actuator_type = actuator_type
        self.actuator_id = actuator_id

class SettingsRequestMessage(Message):
    def __init__(self, key, action, data_type, min_, max_, unit_of_measurement):
        if action == "SET":
            super().__init__("SET SETTINGS", key)
        elif action == "GET":
            super().__init__("GET SETTINGS", key)
        self.data_type = data_type
        self.min = min_
        self.max = max_
        self.unit_of_measurement = unit_of_measurement
        self.protocol = socket.SOCK_DGRAM

class SettingsResponseMessage(Message):
    def __init__(self, key, status, message, data_type, min_, max_, unit_of_measurement):
        super().__init__("RESPONSE SETTINGS", key)
        self.status = status
        self.message = message
        self.data_type = data_type
        self.min = min_
        self.max = max_
        self.unit_of_measurement = unit_of_measurement

class ValueRequestMessage(Message):
    def __init__(self, key, data_type, unit_of_measurement):
        super().__init__("GET VALUE", key)
        self.data_type = data_type
        self.unit_of_measurement = unit_of_measurement
        self.protocol = socket.SOCK_DGRAM

class ValueResponseMessage(Message):
    def __init__(self, key, status, message, data_type, value, unit_of_measurement):
        super().__init__("RESPONSE VALUE", key)
        self.status = status
        self.message = message
        self.data_type = data_type
        self.value = value
        self.unit_of_measurement = unit_of_measurement

def send_request(HOST, port, message, timeout=5):
    logger.debug(f'Sending request to {HOST}:{port} - {message}')
    if message.protocol == socket.SOCK_DGRAM:  # UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.settimeout(timeout)
            client_socket.sendto(json.dumps(message.__dict__).encode(), (HOST, port))
            try:
                response, addr = client_socket.recvfrom(1024)
                response_message = response.decode()
                logger.debug(f'Received response from {addr} - {response_message}')
                response_json = response_message  # Convertendo a mensagem de resposta em um objeto JSON válido
            except socket.timeout:
                response_json = {"status": "ERROR", "message": "No response received within the timeout period."}
                logger.debug(f'Timeout: No response received from {HOST}:{port} within {timeout} seconds')
            return response_json
    else:  # TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(timeout)
            try:
                client_socket.connect((HOST, port))
                client_socket.sendall(json.dumps(message.__dict__).encode())
                response = client_socket.recv(1024)
                response_message = response.decode()
                logger.debug(f'Received response from {HOST}:{port} - {response_message}')
                response_json = response_message  # Convertendo a mensagem de resposta em um objeto JSON válido
            except socket.timeout:
                response_json = {"status": "ERROR", "message": "No response received within the timeout period."}
                logger.debug(f'Timeout: No response received from {HOST}:{port} within {timeout} seconds')
            return response_json
