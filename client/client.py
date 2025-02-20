import threading
import socket

class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        self.__host = host
        self.__port = port
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          
          
    def receive_messages(self):
        while True:
            try:
                msg = self.__client_sock.recv(1024).decode()
                if msg.upper() == 'ENDC' or not msg:
                    break
                print(f"Servidor: {msg}")
            except (ConnectionResetError, ConnectionAbortedError):
                break
            
        print("Encerrando conexão...")
        self.__client_sock.close()
        

    def send_messages(self):
        while True:
            msg = input("> ")
            if msg.lower() in ['exit', 'quit', 'sair']:
                break
            try: 
                self.__client_sock.sendall(msg.encode()) 
            except:
                break

    def connect_client(self):
        self.__client_sock.connect((self.__host, self.__port))
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()
        print("Conexão encerrada.")
        self.__client_sock.close()


if __name__ == "__main__":
    client = Client()
    client.connect_client()
