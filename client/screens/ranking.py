from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, OptionList
from textual.containers import Horizontal, Vertical


class Ranking(Screen[dict[str, str]]):

    def __init__(self, game_leader: bool, players: list[str]) -> None:
        super().__init__()
        self.__game_leader = game_leader
        self.__players = players

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            OptionList(*self.__gen_ranks(), id="ranking-list", wrap=True),
            Horizontal(
                Button(
                    "Restart" if self.__game_leader else "Continue",
                    classes="ranking-button",
                    id="restart-button",
                ),
                Button("Quit", classes="ranking-button", id="continue-button"),
                id="ranking-horizontal",
            ),
            id="ranking-main",
        )
        yield Footer()

    def __gen_ranks(self):
        for player in self.__players:
            yield player
            yield None

    @on(Button.Pressed, '#continue-button')
    def handle_continue_game(self) -> None:
        # _input = self.query_one(Input)

        # self.dismiss(_input.value)
        ...
    
    @on(Button.Pressed, '#restart-button')
    def handle_restart_game(self) -> None:
        # _input = self.query_one(Input)

        # self.dismiss(_input.value)
        ...
