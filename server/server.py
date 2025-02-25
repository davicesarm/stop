import threading
import socket
import json
from data_structures.bst import BinarySearchTree
from potstop import Potstop
import time

class Client:
    def __init__(self, socket, address, name = ""):
        self.socket = socket
        self.address = address
        self.name = name

    def __eq__(self, other: "Client") -> bool:
        return self.address == other.address
    
    def __lt__(self, other: "Client") -> bool:
        return self.address < other.address

class Server:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clients = BinarySearchTree()
        self.__potstop = Potstop()

    def start(self):
        self.__server_sock.bind((self.__host, self.__port))
        self.__server_sock.listen(10)
        threading.Thread(target=self.stop_server, daemon=True).start()
        
        print(f"[+] Servidor escutando em {self.__host}:{self.__port}")
        
        while True:
            try:
                client_sock, address = self.__server_sock.accept()
                client = Client(client_sock, address)
                self.__clients.add(client)
                threading.Thread(target=self.handle_client_requests, args=(client,), daemon=True).start()
            except (OSError, KeyboardInterrupt):
                break
    
    def handle_client_requests(self, client: Client):
        while True:
            try:
                msg: str = client.socket.recv(1024).decode()
                if not msg:
                    break
                
                response = self.handle_message(client, msg)
                client.socket.sendall(f"{response}".encode())
                if msg.startswith('QUIT'):
                    break
            except ConnectionResetError:
                break
        
        print(f"[-] Conexão encerrada com {client.address}")
        self.__clients.delete(client)
        client.socket.close()
        
    def validate_stop(self):
        while self.__potstop.game_started:
            while not self.__potstop.stop_queue.is_empty():
                stop: tuple[Client, dict] = self.__potstop.stop_queue.dequeue()
                if self.__potstop.is_stop_valid(stop[1]):
                    self.__potstop.stop()
                    self.__potstop.stop_queue.clear()
                    self.__potstop.end_game()
                    stop[0].socket.sendall("10 Stopped".encode())
                else:
                    stop[0].socket.sendall("14 Stop Failed".encode())
            time.sleep(0.1)
        
        time.sleep(0.2)
        self.broadcast("STOP")
        timeout = 0
        while timeout < 10 and len(self.__potstop.answers) < len(self.__potstop.get_players()):
            time.sleep(0.5)
            timeout += 1
        answers = [data for _, data in self.__potstop.answers]
        words = self.__potstop.count_words(answers)
        for name, ans in self.__potstop.answers:
            self.__potstop.compute_points(name, ans, words)
        print(self.__potstop.get_ranking())


    def handle_message(self, client: Client, msg: str):
        if msg.startswith("QUIT"):
            self.__potstop.remove_player(client.name)
            return "30 Left"
        elif msg.startswith('START'):
            if self.__potstop.game_started:
                return "42 Impossible"
            if self.__potstop.get_leader() != client.name:
                return "41 Unauthorized"
            self.__potstop.start_game()
            threading.Thread(target=self.validate_stop, daemon=True).start()
            return "40 Started"
        elif msg.startswith('JOIN'):
            try:
                name = msg.split('\n')[1].strip()
            except IndexError:
                return "0 Bad Request"
            if name in self.__potstop.get_players() or name.upper() == "SERVER":
                return "22 Already Joined"

            self.__potstop.add_player(name, 0)
            client.name = name
            return "20 Joined"
        elif msg.startswith('STOP'):
            try:
                data = json.loads(msg.strip().split('\n')[1])
            except json.JSONDecodeError:
                return "0 Bad Request"
            
            # Adicionar verificao caso tenha tentado dar stop sem o jogo ter começado

            if not self.__potstop.stopped:
                self.__potstop.stop_queue.enqueue((client, data))
                return "11 Verifying Stop"
            else:
                self.__potstop.answers.append((client.name, data))
                return "10 Stopped"
            
        else:
            return "0 Bad Request"


    def kill_clients(self):
        if not self.__clients.isEmpty():
            for client in self.__clients:
                client.socket.sendall("ENDC".encode())
                client.socket.close()


    def stop_server(self):
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
        self.kill_clients()

    def broadcast(self, msg: str):
        for client in self.__clients:
            client.socket.sendall(msg.encode())

if __name__ == "__main__":
    Server().start()
