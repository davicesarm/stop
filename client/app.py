import json
import logging

from typing import Optional, TypedDict, cast
from textual.app import App

from client.screens import Entry, Game, Ranking, Waiting
from client.client import Client

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s" + "\n",
    filename="log-app.txt",
    encoding="utf-8",
)

class StartData(TypedDict):
    round: int
    pots: list[str]
    letter: str


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"

    def __init__(self, server_host: str = "localhost", server_port: int = 8888):
        super().__init__()

        self.__server_host = server_host
        self.__server_port = server_port
        self.game_letter: str = ""
        self.game_pots: list[str] = []
        self.game_round = 0

    def on_mount(self) -> None:
        self.theme = "dracula"
        self.__client_socket = Client(
            server_host=self.__server_host,
            server_port=self.__server_port,
            on_message=self.handle_server_messages,
        )
        self.push_screen(Entry(), self.send_username)

    def send_username(self, username: Optional[str]) -> None:
        assert username is not None
        response = self.__client_socket.send_username_to_server(username)

        if not int(response[0]):
            self.push_screen(Waiting(), self.send_start)  # type: ignore
            self.title = "Playing potstop as " + username
            self.notify("You joined the game!")
        else:
            if response[0][0] == "1":
                self.push_screen(Waiting(full_lobby=True))
                return

            self.push_screen(Entry(), self.send_username)
            self.notify(response[1])

    def send_first_stop(self):
        response = self.__client_socket.send_stop_to_server()

        if response[0][0] == "1":
            self.notify("You stopped the game!")

        self.notify(response[1])

    def send_start(self, _: None = None) -> None:
        self.push_screen(Waiting(), self.send_start)

        response = self.__client_socket.send_start_to_server()

        if response[0]:
            self.notify(response[1])

    def send_pots(self, pots: Optional[dict[str, str]]) -> None:
        assert pots is not None
        response = self.__client_socket.send_stop_to_server(pots)
        
        logging.info(f"Failed to handle server message with: {response}")

        if not int(response[0]):
            self.push_screen(
                Ranking(players=json.loads(response[1].split("\n")[1])),
                self.handle_ranking_action,
            )
            return

        self.notify(response[1])

    def handle_ranking_action(self, action: Optional[str]):
        if action == "restart":
            self.send_start()
        else:
            self.notify("Quitting the game!", timeout=3)
            self.exit()  # type: ignore

    def handle_server_messages(self, message: str):
        splitted_message = message.split("\n")
        try:
            if splitted_message[0] == "START":
                data: StartData = json.loads(splitted_message[1])

                def change_start_data():
                    self.game_letter = data["letter"]
                    self.game_pots = data["pots"]
                    self.game_round = data["round"]
                    self.sub_title = f"round -> {self.game_round}"

                self.call_from_thread(change_start_data)

                self.call_from_thread(
                    self.push_screen,
                    Game(
                    pots=self.game_pots,
                    game_letter=self.game_letter,
                    on_stop=self.send_first_stop,
                    ),
                    self.send_pots,
            )
            elif splitted_message[0].startswith("STOPPED") and isinstance(
            self.screen, Game
            ):
                game = cast(Game, self.screen)
                self.call_from_thread(game.get_pots_and_dismiss)
            else:
                self.call_from_thread(self.notify, {message})
        except Exception as e:
            logging.exception(f"Failed to handle server message with: {str(e)}")


if __name__ == "__main__":
    app = Potstop()
    app.run(inline=True)
