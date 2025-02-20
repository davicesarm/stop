import threading
import socket

class Server:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clients = []

    def handle_client(self, client_socket, address):
        print(f"[+] Nova conexão de {address}")
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if not msg:
                    break
                print(f"[{address}] {msg}")
                client_socket.sendall(f"{msg}".encode())
            except ConnectionResetError:
                break
        
        print(f"[-] Conexão encerrada com {address}")
        self.__clients.remove(client_socket)
        client_socket.close()

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
        for client in self.__clients:
            client.sendall("ENDC".encode())
            client.close()

    def start(self):
        self.__server_sock.bind((self.__host, self.__port))
        self.__server_sock.listen(10)
        threading.Thread(target=self.stop_server, daemon=True).start()
        
        print(f"[+] Servidor escutando em {self.__host}:{self.__port}")
        
        while True:
            try:
                client_sock, address = self.__server_sock.accept()
                self.__clients.append(client_sock)
                client_thread = threading.Thread(target=self.handle_client, args=(client_sock, address), daemon=True)
                client_thread.start()
            except (OSError, KeyboardInterrupt):
                break

if __name__ == "__main__":
    server = Server()
    server.start()
