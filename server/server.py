import threading
import socket
import json
from potstop import Potstop
import time
from typing import Optional

class Client:
    """ 
    Class to represent a client connected to the server.
    
    Attributes:
        socket (socket): The client's socket object.
        address (tuple[str, int]): The client's address as a tuple of host and port.
        name (str): The client's name, if any.
    """
    
    def __init__(self, socket: socket, address: tuple[str, int], name: str = "") -> None:
        self.socket = socket
        self.address = address
        self.name = name

    def __eq__(self, other: "Client") -> bool:
        return self.address == other.address
    
class Server:
    def __init__(self):
        self.__host = "0.0.0.0"
        self.__port = 8888
        self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.__clients: list[Client] = []
        self.__potstop = Potstop()
        
    def start(self):
        """
        Starts the server to accept client connections.

        This method binds the server socket to the specified host and port, listens
        for incoming connections, and spawns a thread to handle each client request.
        It also starts a separate thread to monitor for server shutdown requests.

        Raises:
            OSError: If there is an issue with the server socket.
            KeyboardInterrupt: If the server is manually interrupted.
        """

        self.__server_sock.bind((self.__host, self.__port))
        self.__server_sock.listen(10)
        threading.Thread(target=self.__stop_server, daemon=True).start()
        
        print(f"[+] Servidor escutando em {self.__host}:{self.__port}")
        
        while True:
            try:
                client_sock, address = self.__server_sock.accept()
                client = Client(client_sock, address)
                self.__clients.append(client)
                threading.Thread(target=self.__handle_client_requests, args=(client,), daemon=True).start()
            except (OSError, KeyboardInterrupt):
                break
    
    def broadcast(self, msg: str, exclude: Optional[set[str]] = None) -> None:
        """
        Broadcasts a message to all connected clients, optionally excluding
        some by their name.

        Args:
            msg (str): The message to be broadcasted.
            exclude (set[str], optional): A set of client names to be excluded
                from the broadcast. Defaults to None.
        """
        
        if exclude is None:
            exclude = set()
        
        for client in self.__clients:
            if client.name == '' or client.name in exclude: 
                continue
            client.socket.sendall(msg.encode())
            print(f"<BROADCAST> [{client.name or client.address}] {repr(msg)[1:-1]}")
    
    def __handle_client_requests(self, client: Client) -> None:
        """
        Handles client requests.

        This function will run in its own thread and wait for incoming messages
        from the client. When a message is received, it will be processed and a
        response will be sent back to the client.

        Args:
            client (Client): The client object that sent the message.

        Raises:
            ConnectionResetError: If the client disconnects unexpectedly.
        """
        while True:
            try:
                msg: str = client.socket.recv(1024).decode()
                if not msg:
                    break
                
                print(f"> [{client.name or client.address}] {repr(msg)[1:-1]}")
                response = self.__handle_message(client, msg)
                print(f"< [{client.name or client.address}] {repr(response)[1:-1]}")
                client.socket.sendall(f"{response}".encode())
                if msg.startswith('QUIT'):
                    break
            except ConnectionResetError:
                break
        
        print(f"[-] Conexão encerrada com {client.name or client.address}")
        self.__clients.remove(client)
        self.__potstop.remove_player(client.name)
        client.socket.close()
        
    def __handle_message(self, client: Client, data: str) -> str:
        """
        Handles a message from a client.

        This function is responsible for processing incoming messages from
        clients. It will look at the first line of the message and use that as the
        command to execute. The command handler will then receive the rest of the
        message as an argument.

        The handlers for the "JOIN" and "START" commands will receive the entire
        message, including the first line, as an argument. The handlers for the
        "QUIT" and "STOP" commands will only receive the client as an argument.

        If the command is not recognized, the function will return "0 Bad Request".

        Args:
            client (Client): The client that sent the message.
            data (str): The message sent by the client.

        Returns:
            str: The response to the client's message.
        """
        commands = {
            "QUIT": self.__quit,
            "JOIN": self.__join,
            "START": self.__start,
            "STOP": self.__stop    
        }
        
        command = data.split("\n")[0]
        if command not in commands:
            return "0 Bad Request"
        
        if command in ["JOIN", "START"]:
            return commands[command](client, data)
        
        return commands[command](client)
        
    def __quit(self, client: Client) -> str: 
        """
        Handles the client's request to quit the game.

        This method attempts to remove the player associated with the given client
        from the game. If the player is found and successfully removed, a success
        message is returned. If the player is not found, an error message is returned.

        Args:
            client (Client): The client requesting to quit the game.

        Returns:
            str: A response code indicating the result of the quit request. "30 Left"
            if the player was successfully removed, "31 Player Not Found" if the
            player does not exist in the game.
        """

        if self.__potstop.remove_player(client.name) is None:
            return "31 Player Not Found"
        return "30 Left"
    
    def __join(self, client: Client, data: str) -> str:
        """
        Handles the client's request to join the game.

        This method attempts to add the client to the game with the given name. If
        the game is full, the player is already joined, the name is invalid, or the
        game has already started, an error message is returned. If the player is
        successfully added to the game, a success message is returned.

        Args:
            client (Client): The client requesting to join the game.
            data (str): The message sent by the client, which should contain the
                client's desired name on the second line.

        Returns:
            str: A response code indicating the result of the join request. "20
                Joined" if the player was successfully added to the game, "21 Full
                Lobby" if the game is full, "22 Already Joined" if the player is
                already joined, "23 Already Started" if the game has already
                started, "24 Invalid Name" if the name is invalid, or "0 Bad
                Request" if the message is malformed.
        """
        try:
            name = data.split('\n')[1].strip()
        except IndexError:
            return "0 Bad Request"
        if len(self.__potstop.players) >= self.__potstop.player_limit:
            return "21 Full Lobby"
        if name in self.__potstop.players:
            return "22 Already Joined"
        if name == '':
            return "24 Invalid Name"
        if self.__potstop.game_started:
            return "23 Already Started"

        self.__potstop.add_player(name, 0)
        client.name = name
        return "20 Joined"
        
    def __start(self, client: Client) -> str:
        """
        Handles the client's request to start the game.

        This method attempts to start the game. If the game has already started, or
        the client is not the leader, an error message is returned.

        Args:
            client (Client): The client requesting to start the game.

        Returns:
            str: A response code indicating the result of the start request.
            "40 Started" if the game was successfully started, "41 Unauthorized"
            if the client is not the leader, or "42 Already Started" if the game
            has already started.
        """
        
        if self.__potstop.game_started:
            return "42 Already Started"
        if self.__potstop.leader != client.name:
            return "41 Unauthorized"
        self.__potstop.start_game()
        def send_start():
            time.sleep(0.3)
            game_init = {"round": self.__potstop.round, "pots": self.__potstop.pots, "letter": self.__potstop.letter}	
            self.broadcast(f"START\n{json.dumps(game_init)}")
        threading.Thread(target=send_start, daemon=True).start()
        return "40 Started"
    
    def __call_stop(self, client: Client, data: dict[str, str]) -> None:
        """
        Handles a client's stop request.

        Saves the answers from the client that sent the stop request, waits for other
        clients to send their answers (if any), computes points for all clients, and
        finally ends the game and returns the stopped message with the ranking.

        Args:
            client (Client): The client that sent the stop request.
            data (dict[str, str]): The answers from the client.

        Returns:
            str: A response code indicating the result of the stop request.
            "10 Stopped" if the game was successfully stopped, along with the ranking.
        """
        # Salvo as respostas da pessoa que mandou stop
        self.__potstop.answers.append((client.name, data))
        """ 
        Se houver stops simultaneos significa que alguns usuarios
        já enviaram as respostas no primeiro if.
        Então preciso excluí-los do broadcast para evitar erros.
        """
        time.sleep(0.5)
        exclude = {name for name, _ in self.__potstop.answers}
        # Sinalizo que houve um stop para os clientes
        self.broadcast("STOPPED BY " + client.name, exclude=exclude)
        
        # Aguardo as respostas chegarem (se demorar muito eu passo direto)
        start_time = time.time()
        while (time.time() - start_time) < 5 and len(self.__potstop.answers) < len(self.__potstop.players):
            time.sleep(0.5)
        
        # Crio uma lista de respostas list[dict[str, str]]
        # e computo os pontos
        answers = [data for _, data in self.__potstop.answers]
        words = self.__potstop.count_words(answers)
        for name, ans in self.__potstop.answers:
            self.__potstop.compute_points(name, ans, words)
        
        # Enfim finalizo o jogo e retorno stopped e o ranking
        self.__potstop.end_game()
        return f"10 Stopped\n{json.dumps(self.__potstop.ranking)}"
    
    
    def __stop(self, client: Client, data: str) -> str:
        """
        Handle a stop request from a client.

        If the game has not started, returns "11 Not Started".
        If the request is invalid, returns "0 Bad Request".

        If the game has already been stopped, adds the client's
        answers to the list of answers and waits for the points
        to be computed. Then returns "10 Stopped" with the ranking.

        Otherwise, stops the game and calls __call_stop to handle
        the stop request.

        Args:
            client (Client): The client that sent the stop request.
            data (str): The answers from the client.

        Returns:
            str: A response code indicating the result of the stop request.
            "11 Not Started" if the game has not started.
            "0 Bad Request" if the request is invalid.
            "10 Stopped" if the game was successfully stopped, along with the ranking.
        """
        if not self.__potstop.game_started:
            return "11 Not Started"
        
        try:
            data = json.loads(data.strip().split('\n')[1])
        except (json.JSONDecodeError, IndexError):
            return "0 Bad Request"

        # Se ja tiverem dado stop entao vai entrar nesse if
        if self.__potstop.stopped:
            # Manda as respostas e aguarda o jogo acabar
            # (quando terminar de computar os pontos o estado muda) linha 146
            self.__potstop.answers.append((client.name, data))
            start_time = time.time()
            while (time.time() - start_time) < 7.5 and self.__potstop.game_started:
                time.sleep(0.5)
            return f"10 Stopped\n{json.dumps(self.__potstop.ranking)}"
        
        # Dou stop, para garantir que proximo entre no if
        self.__potstop.stop()
        
        return self.__call_stop(client, data)

        
    def __kill_clients(self) -> None:
        """
        Closes all connected clients' sockets and sends the 
        "ENDC" message to them, indicating that the server 
        is shutting down.
        """
        for client in self.__clients:
            client.socket.sendall("ENDC".encode())
            client.socket.close()

    def __stop_server(self) -> None:
        """
        Starts an infinite loop that waits for the user to enter 
        'q' to stop the server. When 'q' is entered, the server 
        socket is closed and all connected clients are terminated.
        """
        
        while True:
            print("Digite 'q' para encerrar o servidor.")
            try:
                command = input()
            except EOFError:
                command = 'q'
                
            if command.strip().lower() == 'q':
                print("Encerrando servidor...")
                break
        
        self.__server_sock.close()
        self.__kill_clients()


if __name__ == "__main__":
    Server().start()
