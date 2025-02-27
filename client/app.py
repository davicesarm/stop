import threading
from typing import Optional
from textual.app import App

# from textual.containers import VerticalScroll
from client.screens import Entry, Game, Ranking, Waiting
from client.client import Client


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"
    POTS = [
        "CEP",
        "MSÉ",
        "Ator",
        "Nome",
        "Música",
        "Carro",
        "Comida",
        "Objeto",
        "Verbo",
        "Utensílio de cozinha",
    ]
    SCREENS = {"entry": Entry}
    PLAYERS = [
        "arthurjosemariodasilvasnatos - 21",
        "mari - 19",
        "cclaras - 14",
        "davis - 13",
    ]

    def __init__(self, server_host: str = "localhost", server_port: int = 8888):
        super().__init__()

        self.title = "Potstop"
        self.__server_host = server_host
        self.__server_port = server_port
        self.game_letter = "A"
        # estado de inicio da partida e logica de implementaçaõ

    def on_mount(self) -> None:
        self.theme = "dracula"
        self.__client_socket = Client(
            server_host=self.__server_host,
            server_port=self.__server_port,
            on_message=self.handle_server_messages,
        )
        self.push_screen("entry", self.send_username)
        # self.push_screen(Ranking(game_leader=True, players=self.PLAYERS))

    def send_username(self, username: Optional[str]) -> None:
        assert username is not None
        response = self.__client_socket.send_username_to_server(username)

        if not response[0]:
            self.push_screen(Waiting(), self.send_start)  # type: ignore
            self.sub_title = username
            self.notify("You joined the game!")
            self.notify("Waiting for game to start!", timeout=10.0)
        else:
            if response[0] == 1:
                self.push_screen(Waiting(full_lobby=True))
                return

            self.push_screen("entry", self.send_username)
            self.notify(response[1])

    def send_start(self, _: None = None) -> None:
        self.push_screen(Waiting(), self.send_start)
            
        def send_async():
            response = self.__client_socket.send_start_to_server()

            if response[0]:
                self.call_from_thread(self.notify, response[1])
                
        threading.Thread(target=send_async).start()

    def send_pots(self, pots: Optional[dict[str, str]]) -> None:
        assert pots is not None
        response = self.__client_socket.send_pots_to_server(pots)

        if not response[0]:
            self.push_screen(
                Ranking(game_leader=True, players=self.PLAYERS),
                self.handle_ranking_action,
            )
            self.notify("You stopped the game!")
            self.notify(response[1])
        else:
            self.push_screen(
                Game(pots=self.POTS, game_letter=self.game_letter), self.send_pots
            )
            self.notify(response[1])

        # self.push_screen(Ranking(game_leader=True, players=self.PLAYERS))

    def handle_ranking_action(self, action: Optional[str]):
        if action == "continue":
            self.pop_screen()
            self.push_screen(Waiting(), self.send_start)  # type: ignore
        elif action == "restart":
            self.send_start()
        else:
            self.notify("Quitting the game!", timeout=3)
            self.exit()  # type: ignore

    def handle_server_messages(self, message: str):
        if message == "START":
            # self.call_from_thread(self.pop_screen)
            self.call_from_thread(
                self.push_screen,
                Game(pots=self.POTS, game_letter=self.game_letter),
                self.send_pots,
            )
        else:
            self.call_from_thread(self.notify, f"{message}")


if __name__ == "__main__":
    app = Potstop()
    app.run()
