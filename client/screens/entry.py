from typing import Optional
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Input, Button, Header, Footer
from textual.containers import Vertical


class Entry(Screen[tuple[str, str]]):
    def __init__(self, username: Optional[str] = None):
        self.__username = username
        super().__init__()
        

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Input(placeholder="Seu nome",value=self.__username,classes="entry-input", valid_empty=False, id='entry-name'),
            Input(placeholder="192.168.0.1:8888", classes="entry-input", id='entry-address'),            
            Button("Entrar", classes="entry-button"),
            id="entry-main",
        )
        yield Footer()

    @on(Input.Submitted)
    @on(Button.Pressed)
    def handle_entry_sent(self) -> None:
        name = self.query_one('#entry-name', Input)
        address = self.query_one('#entry-address', Input)        
        
        if name.value == '':
            self.notify('Invalid username: empty!')
        else:
            self.dismiss((name.value.strip(), address.value.strip()))
