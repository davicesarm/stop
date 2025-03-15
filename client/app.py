import json
import logging

from typing import Optional, TypedDict, cast
from textual.app import App

from client.screens import Entry, Game, Ranking, Waiting
from client.client import Client

class StartData(TypedDict):
    round: int
    pots: list[str]
    letter: str


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"

    def __init__(self):
        super().__init__()
        self.game_letter: str = ""
        self.game_pots: list[str] = []
        self.game_round = 0
        self.__client_socket = Client(self.handle_server_messages)

    def on_mount(self) -> None:
        self.theme = "dracula"

        self.push_screen(Entry(), self.send_username)

    def send_username(self, infos: Optional[tuple[str, Optional[str]]]) -> None:
        assert infos is not None

        if infos[1]:
            address = infos[1].split(":")
            
            self.__client_socket.connect(
                address[0],
                int(address[1]) if len(address) > 1 and address[1].isdigit() else None,
            )
        else:
            self.__client_socket.connect()
            
        response = self.__client_socket.send_username_to_server(infos[0])            

        if not int(response[0]):
            self.push_screen(Waiting(), self.send_start)  # type: ignore
            self.title = "Playing potstop as " + infos[0]
            self.notify("You joined the game!")
        else:
            if response[0][0] == "1":
                self.push_screen(Waiting(full_lobby=True))
                return

            self.push_screen(Entry(), self.send_username)
            self.notify(response[1])

    def send_start(self, _: None = None) -> None:
        self.push_screen(Waiting(), self.send_start)

        response = self.__client_socket.send_start_to_server()

        if response[0]:
            self.notify(response[1])

    def send_pots(self, pots: Optional[dict[str, str]]) -> None:
        assert pots is not None
        response = self.__client_socket.send_stop_to_server(pots)

        if not int(response[0]):
            self.push_screen(
                Ranking(players=json.loads(response[1].split("\n")[1])),
                self.handle_ranking_action,
            )

        self.notify(response[1].split('\n')[0])

    def handle_ranking_action(self, action: Optional[str]):
        if action == "restart":
            self.send_start()
        else:
            response = self.__client_socket.send_quit_to_server()
            
            if not int(response[0]):
                self.notify("Quitting the game!", timeout=3)
                self.exit()  # type: ignore
            
            self.notify('Error trying to quit the game!')          

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
                    ),
                    self.send_pots,
                )

            elif splitted_message[0].startswith("STOPPED") and isinstance(
                self.screen, Game
            ):
                game = cast(Game, self.screen)
                self.call_from_thread(game.get_pots_and_dismiss)
            else:
                self.call_from_thread(self.notify, str(message))
        except Exception as e:
            logging.exception(f"Failed to handle server message with: {str(e)}")


if __name__ == "__main__":
    app = Potstop()
    app.run()
