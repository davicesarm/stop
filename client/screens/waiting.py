from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, LoadingIndicator, Button, Label
from textual.containers import Vertical


class Waiting(Screen[None]):
    
    def __init__(self, full_lobby: bool = False):
        super().__init__()
        self.__full_lobby = full_lobby

    def compose(self) -> ComposeResult:
        my_button = Button('Start game!')
        my_button.can_focus = False
        
        yield Header()
        yield Vertical(
            LoadingIndicator(id='waiting-loading'),
            my_button if not self.__full_lobby else Label('Full lobby...'),
            id='waiting-main'
        )
        yield Footer()

    @on(Button.Pressed)
    def handle_game_start(self) -> None:
        self.dismiss()