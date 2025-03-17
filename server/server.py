import threading
import socket
import json
from potstop import Potstop
import time

class Client:
    def __init__(self, socket: socket, address: tuple[str, int], name=""):
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
        self.__clients = []
        self.__potstop = Potstop()

    def start(self):
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
    
    def broadcast(self, msg: str, exclude: set = None) -> None:
        if exclude is None:
            exclude = set()
        
        for client in self.__clients:
            if client.name == '' or client.name in exclude: 
                continue
            client.socket.sendall(msg.encode())
            print(f"<BROADCAST> [{client.name or client.address}] {repr(msg)[1:-1]}")
    
    def __handle_client_requests(self, client: Client) -> None:
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
        if self.__potstop.remove_player(client.name) is None:
            return "31 Player Not Found"
        return "30 Left"
    
    def __join(self, client: Client, data: str) -> str:
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
        for client in self.__clients:
            client.socket.sendall("ENDC".encode())
            client.socket.close()

    def __stop_server(self) -> None:
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
