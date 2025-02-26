from typing import Optional
from textual.app import App

# from textual.containers import VerticalScroll
from client.screens import Entry, Game, Ranking, Waiting
from client.client import Client


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"
    POTS = ['CEP', 'MSÉ', 'Ator', 'Nome', 'Música', 'Carro', 'Comida', 'Objeto', 'Verbo', 'Utensílio de cozinha']
    SCREENS = {"entry": Entry, "waiting": Waiting}
    PLAYERS = ['arthur - 21', 'mari - 19', 'cclaras - 14', 'davis - 13']
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8888):
        super().__init__()
        
        self.title = 'Potstop'
        self.__server_host = server_host
        self.__server_port = server_port
        # estado de inicio da partida e logica de implementaçaõ

    def on_mount(self) -> None:
        self.theme = "dracula"
        self.__client_socket = Client(
            server_host=self.__server_host,
            server_port=self.__server_port,
            on_message=self.handle_server_messages,
        )
        self.push_screen('entry', self.send_username)
        
    def send_username(self, username: Optional[str]) -> None:           
        assert username is not None

        response = self.__client_socket.send_username_to_server(username)
        self.sub_title = username
        
        if not response[0]:
            # self.push_screen(c)
            self.push_screen(Waiting(self.send_start))
            self.notify(f"{username} joined the game!")
            self.notify('Waiting for game to start!', timeout=10.0)
        else:
            self.push_screen('entry', self.send_username)
            self.notify(response[1])
            
    def send_start(self) -> None:
        self.__client_socket.send_start_to_server()
            
    def send_pots(self, pots: Optional[list[str]]) -> None:
        #TODO: create send pots logic
                        
        self.push_screen(Ranking(game_leader=True, players=self.PLAYERS))
        
    def handle_server_messages(self, message: str):
        if message == "START":
            # self.call_from_thread(self.pop_screen)
            self.call_from_thread(self.push_screen, Game(pots=self.POTS), self.send_pots)
        # self.call_from_thread(self.notify, message)

if __name__ == "__main__":
    app = Potstop()
    app.run()