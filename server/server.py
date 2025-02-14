import asyncio
import socket

class Server:
  def __init__(self, host="127.0.0.1", port=8888):
    self.__host = host
    self.__port = port
    self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.__server_sock.setblocking(False)

  async def handle_client(self, client_sock):
    """Lida com a comunicação com um cliente."""
    addr = client_sock.getpeername()
    print(f"Conexão aceita de {addr}")

    try:
        while True:
            data = await asyncio.get_running_loop().sock_recv(client_sock, 1024)
            if not data:
                print(f"Cliente {addr} desconectou.")
                break

            print(f"Recebido de {addr}: {data.decode()}")
            await asyncio.get_running_loop().sock_sendall(client_sock, data)
    except Exception as e:
        print(f"Erro na conexão com {addr}: {e}")
    finally:
        client_sock.close()

  async def start(self):
    """Inicia o servidor e aceita conexões assíncronas."""
    self.__server_sock.bind((self.__host, self.__port))
    self.__server_sock.listen(100)
    print(f"Servidor rodando em {self.__host}:{self.__port}")

    loop = asyncio.get_running_loop()
    while True:
      client_sock, _ = await loop.sock_accept(self.__server_sock)
      asyncio.create_task(self.handle_client(client_sock))


if __name__ == "__main__":
  server = Server()
  asyncio.run(server.start())
