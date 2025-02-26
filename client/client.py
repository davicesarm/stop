import threading
import socket
import time
from typing import Callable, Optional

class Client:
    def __init__(self, on_message: Callable[[str], None], server_host: str = 'localhost', server_port: int = 8888):
        self.__server_host = server_host
        self.__server_port = server_port
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__on_message = on_message
        self.__pending_responses: dict[str, Optional[str]] = {}
        self.__lock = threading.Lock()
        threading.Thread(target=self.__connect_client, daemon=True).start()
    
    def send_username_to_server(self, username: str) -> tuple[int, str]:
        try:
            message = f"JOIN\n{username}"
            self.__pending_responses['JOIN'] = None
            
            self.__client_sock.sendall(message.encode())
            
            response = self.__retrieve_response('JOIN')
            
            
            return response
            
        except Exception as e:
            return (1, f'Ocorreu um erro: ({e.__str__()})! Tente novamente.')
    
    def send_start_to_server(self) -> None:
        try:         
            self.__client_sock.sendall('START'.encode())            
                        
        except Exception as e:
             threading.Thread(target=self.__on_message, args=(f'Ocorreu um erro: ({e.__str__()})! Tente novamente.')).start()
        
    def __retrieve_response(self, request_method: str, timeout: int = 2):
        started_at = time.time()
        
        while time.time() - started_at < timeout:
            with self.__lock:
                if self.__pending_responses[request_method] is not None:
                    response = self.__pending_responses.pop(request_method)
                    assert response is not None
                    return (0 if response[1] == '0' else 1, response[3:])
            
            time.sleep(0.2)

        return (0, 'Tempo limite para resposta do servidor!')
          
    def __receive_messages(self):        
        while True:
            try:
                msg = self.__client_sock.recv(1024).decode()
                # self.__on_message(msg)
                
                if msg.upper() == 'ENDC' or not msg:
                    break
                
                if msg[0].isdigit():
                    if msg[0] == '2':
                        with self.__lock:
                            self.__pending_responses['JOIN'] = msg
                    if msg[0] == '4':
                        with self.__lock:
                            self.__pending_responses['START'] = msg
                else:
                    self.__on_message(msg)
                
            except (ConnectionResetError, ConnectionAbortedError):
                break
            
        self.__client_sock.close()
        self.__reconnect_client()

    def __connect_client(self):
        try:
            self.__client_sock.connect((self.__server_host, self.__server_port))
            threading.Thread(target=self.__receive_messages, daemon=True).start()
        
        except Exception:
            self.__reconnect_client()
        
    def __reconnect_client(self):
        tried = False
        
        while True:            
            try:
                self.__on_message(f'{'Problemas de conexão com o servidor, t' if not tried else 'T'}entando reconectar...')
                self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__client_sock.connect((self.__server_host, self.__server_port))
                self.__on_message('Conexão reestabelecida!')
                threading.Thread(target=self.__receive_messages, daemon=True).start()
                
                break
            except Exception:
                time.sleep(5)
            tried = True
