from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, ListView, ListItem, Label
from textual.containers import Horizontal, Vertical
from typing import Union


class Ranking(Screen[str]):

    def __init__(self, players: list[list[Union[str, int]]]) -> None:
        super().__init__()
        self.__players = players

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            ListView(*self.__gen_ranks(), id="ranking-list"),
            Horizontal(
                Button(
                    "Restart",
                    classes="ranking-button",
                    id="main-button",
                ),
                Button("Quit", classes="ranking-button", id="continue-button"),
                id="ranking-horizontal",
            ),
            id="ranking-main",
        )
        yield Footer()

    def __gen_ranks(self):
        for player, points in self.__players:
            yield ListItem(Label(f'{player} - {points}'), classes='ranking-item')

    @on(Button.Pressed)
    def handle_continue_game(self, event: Button.Pressed) -> None:
        self.dismiss(str(event.button.label).lower())
