from typing import Callable
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, LoadingIndicator, Button
from textual.containers import Vertical


class Waiting(Screen[str]):
    
    def __init__(self, send_start: Callable[[], None]):
        super().__init__()
        self.__send_start = send_start

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            # LoadingIndicator(),
            Button('Start game!'),
            id='waiting-main'
        )
        yield Footer()

    @on(Button.Pressed)
    def handle_game_start(self) -> None:
        self.__send_start()