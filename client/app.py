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
        """A listener of the mount event.
        
        When the Textual app mounts, select the Dracula theme and do the Entry screen push.
        """
        self.theme = "dracula"

        self.push_screen(Entry(), self.send_username)

    def send_username(self, infos: Optional[tuple[str, Optional[str]]]) -> None:
        """Ask the client to connect with the server and handles the answer.
        
        Args:
            infos (Optional[tuple[str, Optional[str]]]): A tuple containing the username 
                and an optional server address in the format "host:port". If the address 
                is not provided, a default connection is attempted.
                
        Raises:
            AssertionError: If `infos` is None.

        Behavior:
            - If a server address is provided, it splits the address into host and port 
              and attempts to connect to the server. If the port is invalid or missing, 
              it defaults to None.
            - Sends the username to the server and processes the server's response.
            - Depending on the server's response:
                - If the response indicates success, it transitions to the "Waiting" screen 
                  and updates the title and notification.
                - If the response indicates a full lobby, it transitions to the "Waiting" 
                  screen with a full lobby indicator.
                - If the response indicates an error, it transitions back to the "Entry" 
                  screen and displays the error message.
        """
        connected = ''
        assert infos is not None

        if infos[1]:
            address = infos[1].split(":")
            
            connected = self.__client_socket.connect(
                address[0],
                int(address[1]) if len(address) > 1 and address[1].isdigit() else None,
            )
        else:            
            connected = self.__client_socket.connect()
            
        if connected and connected.startswith('ERROR:'):
            self.push_screen(Entry(infos[0]), self.send_username)
            self.notify(connected[7:])
            return
            
        response = self.__client_socket.send_username_to_server(infos[0])            

        if not int(response[0]):
            self.push_screen(Waiting(), self.send_start)  # type: ignore
            self.title = "Playing potstop as " + infos[0]
            self.notify("You joined the game!")
        else:
            if response[0][0] == "1":
                self.push_screen(Waiting(full_lobby=True))
                return

            self.push_screen(Entry(infos[0]), self.send_username)
            self.notify(response[1])

    def send_start(self, _: None = None) -> None:
        """
        Initiates the start process by pushing a waiting screen and sending a start 
        request to the server.

        Args:
            _: Optional; Default is None. Placeholder argument for compatibility.

        Returns:
            None
        """
        
        self.push_screen(Waiting(), self.send_start) 

        response = self.__client_socket.send_start_to_server()

        if response[0]:
            self.notify(response[1])

    def send_pots(self, pots: Optional[dict[str, str]]) -> None:
        """
        Call the client to send the pots to the server and stop the game.

        Args:
            pots (Optional[dict[str, str]]): A dictionary containing pots data to be sent to the server.
                                             The keys and values are strings. Must not be None.

        Raises:
            AssertionError: If `pots` is None.

        Behavior:
            - Sends the `pots` dictionary to the server using the client socket.
            - If the server response indicates success (response[0] evaluates to True):
                - Pushes the `Ranking` screen with the players' data parsed from the server response.
            - Notifies the user with the first line of the server response.
        """
        
        assert pots is not None
        response = self.__client_socket.send_stop_to_server(pots)

        if not int(response[0]):
            self.push_screen(
                Ranking(players=json.loads(response[1].split("\n")[1])),
                self.handle_ranking_action,
            )

        self.notify(response[1].split('\n')[0])

    def handle_ranking_action(self, action: Optional[str]):
        """
        Handles the ranking action based on the provided action string.
        Args:
            action (Optional[str]): The action to be performed. 
                                    If "restart", the game will restart.
                                    If any other value, an attempt to quit the game is made.
        Behavior:
            - If the action is "restart", it triggers the game restart process.
            - If the action is not "restart", it sends a quit request to the server.
            - If the quit request is successful, it notifies the user and exits the game.
            - If the quit request fails, it notifies the user of the error.
        """
        
        if action == "restart":
            self.send_start()
        else:
            response = self.__client_socket.send_quit_to_server()
            
            if not int(response[0]):
                self.notify("Quitting the game!", timeout=3)
                self.exit()  # type: ignore
            
            self.notify('Error trying to quit the game!')          

    def handle_server_messages(self, message: str):
        """
        Handles incoming messages from the server and performs appropriate actions 
        based on the message content.
        
        Args:
            message (str): The message received from the server, expected to be 
                           formatted as a string with newline-separated components.
        Behavior:
            - If the message starts with "START", it parses the subsequent JSON data 
              to update game state variables (`game_letter`, `game_pots`, `game_round`) 
              and transitions to the game screen.
            - If the message starts with "STOPPED" and the current screen is a `Game` 
              instance, it retrieves and dismisses the game pots.
            - For other messages, it triggers a notification with the message content.
            
        Raises:
            Exception: Logs any exceptions encountered during message processing.
        """
        
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
