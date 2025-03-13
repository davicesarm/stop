import threading
import socket
import time
from json import dumps
from typing import Callable, Optional


class Client:
    def __init__(
        self,
        on_message: Callable[[str], None],
    ):
        self.__server_host = "localhost"
        self.__server_port = 8888
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__on_message = on_message
        self.__pending_responses: dict[str, Optional[str]] = {}
        self.__lock = threading.Lock()

    def send_username_to_server(self, username: str) -> tuple[str, str]:
        try:
            self.__pending_responses["JOIN"] = None
            self.__client_sock.sendall(f"JOIN\n{username}".encode())

            return self.__retrieve_response("JOIN")
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def send_start_to_server(self) -> tuple[str, str]:
        try:
            self.__pending_responses["START"] = None
            self.__client_sock.sendall("START".encode())

            return self.__retrieve_response("START")
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def send_stop_to_server(
        self, pots: dict[str, str]
    ) -> tuple[str, str]:
        try:
            self.__pending_responses["STOP"] = None
            self.__client_sock.sendall(
                f'STOP\n{dumps(pots)}'.encode()
            )

            response = self.__retrieve_response("STOP")

            return response
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")
        
    def send_quit_to_server(self):
        try:
            self.__pending_responses["QUIT"] = None
            self.__client_sock.sendall(
                'QUIT'.encode()
            )

            response = self.__retrieve_response("QUIT")

            return response
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def __retrieve_response(self, request_method: str, timeout: int = 4):
        started_at = time.time()

        while time.time() - started_at < timeout:
            with self.__lock:
                if self.__pending_responses[request_method] is not None:
                    response = self.__pending_responses.pop(request_method)
                    assert response is not None
                    return (response[1:3].strip(), response[3:])

            time.sleep(0.5)

        # self.__another_on_message(f'pending response: {self.__pending_responses}')
        print("Tempo limite para resposta do servidor!")
        return ("9", "Tempo limite para resposta do servidor!")

    def __receive_messages(self):
        while True:
            try:
                msg = self.__client_sock.recv(1024).decode()

                if msg.upper() == "ENDC" or not msg:
                    break
                
                code = msg[0]

                if code.isdigit():                    
                    response_types = {
                        "1": 'STOP',
                        "2": 'JOIN',
                        "3": 'QUIT',
                        "4": 'START',                        
                    }
                    
                    with self.__lock:
                        self.__pending_responses[response_types[code]] = msg
                            
                else:
                    threading.Thread(target=self.__on_message, args=(msg,), daemon=True).start()

            except (ConnectionResetError, ConnectionAbortedError):
                break

        self.__client_sock.close()
        self.__reconnect_client()

    def connect(self, host: Optional[str] = None, port: Optional[int] = None):
        try:
            self.__client_sock.connect((host or self.__server_host, port or self.__server_port))
            threading.Thread(target=self.__receive_messages, daemon=True).start()

        except Exception:
            self.__on_message("ERROR couldn't connect")

    def __reconnect_client(self):
        tried = False

        while True:
            try:
                self.__on_message(
                    f"{'Problemas de conexão com o servidor, t' if not tried else 'T'}entando reconectar..."
                )
                self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__client_sock.connect((self.__server_host, self.__server_port))
                self.__on_message("Conexão reestabelecida!")
                threading.Thread(target=self.__receive_messages, daemon=True).start()

                break
            except Exception:
                time.sleep(3)
            tried = True
