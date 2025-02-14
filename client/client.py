import asyncio
import socket

class AsyncClient:
  def __init__(self, host='127.0.0.1', port=8888):
    self.host = host
    self.port = port
    self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client_sock.setblocking(False)

  async def start(self):
    """Conecta-se ao servidor e envia uma mensagem."""
    """ loop = asyncio.get_running_loop()
    await loop.sock_connect(self.client_sock, (self.host, self.port))

    message = "Olá, servidor!"
    print(f"Enviando: {message}")
    await loop.sock_sendall(self.client_sock, message.encode())

    data = await loop.sock_recv(self.client_sock, 1024)
    print("Recebido:", data.decode())

    self.client_sock.close() """
    
    try:
      while True:
        loop = asyncio.get_running_loop()
        await loop.sock_connect(self.client_sock, (self.host, self.port))
        
        send_data = input('>')            
        
        while send_data.lower() != 'exit':
          await loop.sock_sendall(self.client_sock, send_data.encode())
          data = await loop.sock_recv(self.client_sock, 1024)
          print("Recebido:", data.decode())
          send_data = input('>')
    except Exception as e:
      print('Erro:', e)
    finally:
      self.client_sock.close()
        
            
          
          

if __name__ == "__main__":
  client = AsyncClient()
  asyncio.run(client.start())
