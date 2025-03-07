import threading
import socket
import time
from json import dumps
from typing import Callable, Optional
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s" + "\n",
    filename="log-client.txt",
    encoding="utf-8",
)


class Client:
    def __init__(
        self,
        on_message: Callable[[str], None],
        server_host: str = "localhost",
        server_port: int = 8888,
    ):
        self.__server_host = server_host
        self.__server_port = server_port
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__on_message = on_message
        self.__pending_responses: dict[str, Optional[str]] = {}
        self.__lock = threading.Lock()
        threading.Thread(target=self.__connect_client, daemon=True).start()
        # self.__connect_client()

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
        self, pots: Optional[dict[str, str]] = None
    ) -> tuple[str, str]:
        try:
            self.__pending_responses["STOP"] = None
            self.__client_sock.sendall(
                f"STOP{'\n' + dumps(pots) if pots else ''}".encode()
            )

            response = self.__retrieve_response("STOP")

            return response
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def __retrieve_response(self, request_method: str, timeout: int = 4):
        started_at = time.time()

        while time.time() - started_at < timeout:
            with self.__lock:
                logging.debug(
                    f"[__retrieve_response] Checando '{request_method}' após {time.time()-started_at:.2f}s; valor atual: {self.__pending_responses[request_method]}"
                )
                if self.__pending_responses[request_method] is not None:
                    response = self.__pending_responses.pop(request_method)
                    logging.info(
                        f"[__retrieve_response] Resposta recebida para '{request_method}': {response}"
                    )
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
                logging.debug(f"[__receive_messages] Mensagem recebida: {msg}")

                if msg.upper() == "ENDC" or not msg:
                    logging.info(
                        "[__receive_messages] Mensagem ENDC ou vazia; encerrando thread de recepção."
                    )
                    break

                if msg[0].isdigit():
                    logging.debug(
                        f"[__receive_messages] Mensagem começa com dígito: {msg[0]}"
                    )
                    if msg[0] == "1":
                        with self.__lock:
                            self.__pending_responses["STOP"] = msg
                            logging.info(
                                f"[__receive_messages] Definida resposta pendente para 'STOP': {msg}"
                            )
                    elif msg[0] == "2":
                        with self.__lock:
                            self.__pending_responses["JOIN"] = msg
                            logging.info(
                                f"[__receive_messages] Definida resposta pendente para 'JOIN': {msg}"
                            )
                    elif msg[0] == "4":
                        with self.__lock:
                            self.__pending_responses["START"] = msg
                            logging.info(
                                f"[__receive_messages] Definida resposta pendente para 'START': {msg}"
                            )
                else:
                    # self.__on_message(msg)
                    def see_thread():
                        logging.info(f"[__see_thread] Chamando on_message com: {msg}")
                        self.__on_message(msg)
                    threading.Thread(target=see_thread, daemon=True).start()
                    logging.info(f"[__receive_messages] Chamando on_message com: {msg}")

            except (ConnectionResetError, ConnectionAbortedError) as e:
                logging.error(f"[__receive_messages] Erro de conexão: {e}")
                break

        logging.info("[__receive_messages] Fechando socket e tentando reconectar...")
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


if __name__ == "__main__":
    c = Client(on_message=print)

    print("sending username")
    c.send_username_to_server("arthur")
    print("sending start")
    c.send_start_to_server()
    print("sending stop")
    c.send_stop_to_server()
