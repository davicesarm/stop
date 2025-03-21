import threading
import socket
import time
import errno
from json import dumps
from typing import Callable, Optional


class Client:
    """Client class for managing communication with a server.    
    
    This class provides methods to send various commands to the server, such as
    joining, starting, stopping, and quitting. It also handles receiving messages
    from the server and reconnecting in case of connection issues.
    """
    
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
        """
        Sends the provided username to the server and waits for a response.

        This method sends a "JOIN" command followed by the username to the server
        through the client socket. It then retrieves the server's response to the
        "JOIN" command. If an error occurs during the process, it returns an error
        code and message.

        Args:
            username (str): The username to send to the server.

        Returns:
            tuple: A tuple containing:
                - A response code as a string (e.g., "20" for success, "99" for error).
                - A response message from the server or an error message.
        """
        
        try:
            self.__pending_responses["JOIN"] = None
            self.__client_sock.sendall(f"JOIN\n{username}".encode())

            return self.__retrieve_response("JOIN")
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def send_start_to_server(self) -> tuple[str, str]:
        """
        Sends a "START" command to the server and waits for a response.

        This method sends a "START" message to the server through the client socket
        and waits for a response associated with the "START" command. If an error
        occurs during the process, it returns an error code and message.

        Returns:
            tuple: A tuple containing:
                - A response code as a string (e.g., "40" for success, "99" for error).
                - A response message from the server or an error message.
        """
        
        try:
            self.__pending_responses["START"] = None
            self.__client_sock.sendall("START".encode())

            return self.__retrieve_response("START")
        except Exception as e:
            return ("99", f"Ocorreu um erro: ({e.__str__()})! Tente novamente.")

    def send_stop_to_server(
        self, pots: dict[str, str]
    ) -> tuple[str, str]:
        """
        Sends a STOP command along with a dictionary of pots to the server.

        This method sends a serialized dictionary of pots to the server using the
        STOP command. It waits for a response from the server and returns it. If
        an error occurs during the process, it returns an error code and message.

        Args:
            pots (dict[str, str]): A dictionary containing pots data to be sent to the server.

       Returns:
            tuple: A tuple containing:
                - A response code as a string (e.g., "10" for success, "99" for error).
                - A response message from the server or an error message.
        """
        
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
        """
        Sends a "QUIT" command to the server and waits for a response.
        
        This method attempts to gracefully notify the server that the client
        is disconnecting by sending a "QUIT" message. It then waits for a 
        response from the server to confirm the operation.
                
        Returns:
            tuple: A tuple containing a status code and a message. 
                - On success, the status code and message are determined by the server's response. 
                - On failure, returns ("99", "Ocorreu um erro: {Erro}! Tente novamente.").
        """
        
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
        """
        Retrieves a response for a given request method within a specified timeout period.

        This method continuously checks for a response associated with the given 
        request method in the `__pending_responses` dictionary. If a response is 
        found within the timeout period, it is returned. Otherwise, a timeout 
        message is returned.

        Args:
            request_method (str): The method name for which the response is being retrieved.
            timeout (int, optional): The maximum time (in seconds) to wait for a response. 
                                     Defaults to 4 seconds.

        Returns:
            tuple: A tuple containing:
                str: The response code (e.g., "9" for timeout).
                str: The response message or an error message if the timeout is reached.

        Raises:
            AssertionError: If the response retrieved from `__pending_responses` is None.
        """
        
        started_at = time.time()

        while time.time() - started_at < timeout:
            with self.__lock:
                if self.__pending_responses[request_method] is not None:
                    response = self.__pending_responses.pop(request_method)
                    assert response is not None
                    return (response[1:2], response[3:])

            time.sleep(0.5)

        return ("9", "Tempo limite para resposta do servidor!")

    def __receive_messages(self):
        """
        Handles receiving messages from the client socket in a continuous loop in a thread.
        
        This method listens for incoming messages from the server and processes them
        based on their content. It supports handling specific response types, invoking
        a callback for general messages, and managing connection errors.
        
        **Message Handling:**
            - If the message starts with a digit, it is treated as a response type
              and stored in the `__pending_responses` dictionary.
            - If the message does not start with a digit, it is passed to the
              `__on_message` callback in a separate thread.
            - If the message is "ENDC" (case-insensitive) or empty, the loop terminates.
            
        **Exceptions:**
            - Handles `ConnectionResetError` and `ConnectionAbortedError` gracefully
              by breaking the loop and closing the socket.
              
        **Post-Processing:**
            - Closes the client socket after exiting the loop.
            - Attempts to reconnect the client by calling `__reconnect_client`.
            
        **Note:**
            This method runs indefinitely until a termination condition is met or
            an exception occurs.
            
        **Raises:**
            None directly, but exceptions during socket operations are caught and handled.
        """
        
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
        """
        Establishes a connection to the server using the specified host and port.

        If no host or port is provided, the method defaults to using the instance's
        predefined server host and port.

        Args:
            host (Optional[str]): The hostname or IP address of the server to connect to.
                                  Defaults to None, which uses the instance's server host.
            port (Optional[int]): The port number of the server to connect to.
                                  Defaults to None, which uses the instance's server port.

        Starts a separate thread to handle incoming messages once the connection is established.

        Raises:
            Exception: If the connection attempt fails, an error message is passed to the
                       `__on_message` method.
        """
        with open('log.txt', 'w') as f:
            f.write(f"{host or self.__server_host} {port or self.__server_port}")
        
        try:
            self.__client_sock.settimeout(1)
            self.__client_sock.connect((host or self.__server_host, port or self.__server_port))
            threading.Thread(target=self.__receive_messages, daemon=True).start()

        except OSError as e:
            msg = ''
            if e.errno in (errno.ECONNREFUSED, errno.EHOSTUNREACH, 11001):
                msg = "ERROR: Connection refused or host unreachable."
            elif e.errno == errno.ETIMEDOUT:
                msg = "ERROR: Connection timed out."
            else:
                msg = f"ERROR: Socket error occurred: {e.strerror or str(e)}"
            self.__client_sock.close()
            self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return msg
        except Exception as e:
            msg = f"ERROR: Unexpected error occurred: {e}"
            self.__on_message(msg)
            self.__client_sock.close()
            self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return msg
        finally:
            self.__client_sock.settimeout(None)

    def __reconnect_client(self):
        """
        Attempts to reconnect the client to the server in case of a disconnection.

        This method runs an infinite loop that continuously tries to establish a connection
        to the server. It creates a new socket, attempts to connect to the server using the
        specified host and port, and starts a thread to handle incoming messages upon a 
        successful connection. If the connection fails, it waits for 3 seconds before retrying.

        Messages are sent to the `__on_message` method to notify about the connection status.

        **Note:**
            This method blocks execution until the connection is successfully reestablished.

        Raises:
            Exception: If an unexpected error occurs during the reconnection process.
        """
        
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
