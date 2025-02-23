from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Input, Button, Header, Footer
from textual.containers import Vertical


class Entry(Screen[str]):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Input(placeholder="Seu nome", classes="entry-input"),
            Button("Entrar", classes="entry-button"),
            id="entry-main",
        )
        yield Footer()

    @on(Input.Submitted)
    @on(Button.Pressed)
    def handle_entry_sent(self) -> None:
        _input = self.query_one(Input)

        self.dismiss(_input.value)
