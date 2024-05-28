import logging
import os

def setup_logging():
    logger = logging.getLogger("socket_logger")
    logger.setLevel(logging.DEBUG)
    
    # Cria um caminho absoluto para o arquivo de log
    log_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'socket_messages.log')
    
    # Cria um handler que escreve em um arquivo
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)
    
    # Cria um formato para as mensagens de log
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Adiciona o handler ao logger
    logger.addHandler(handler)
    
    logger.debug(f'Log file path: {log_file_path}')  # Verifica o caminho do arquivo de log
    return logger
