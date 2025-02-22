from time import monotonic
from textual import on
from textual.screen import Screen
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Button, Header, Footer, Digits
from textual.containers import VerticalScroll, Horizontal, Vertical


class Game(Screen[dict[str, str]]):

    def __init__(
        self,
        pots: list[str],
    ) -> None:
        super().__init__()
        self.__pots = pots

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            VerticalScroll(*self.__gen_pots(self.__pots), id="game-pots"),
            Horizontal(Timer(), Button("POTS", classes="game-button"), id="game-horizontal"),
            id="game-main",
        )
        yield Footer()

    @on(Button.Pressed)
    def handle_game_stopped(self) -> None:
        # _input = self.query_one(Input)

        # self.dismiss(_input.value)
        ...

    def __gen_pots(self, pots: list[str]):
        for pot in pots:
            yield Input(placeholder=pot, classes="pot")
            
            
class Timer(Digits):
    
    start_time: reactive[float] = reactive(monotonic)
    elapsed_time: reactive[float] = reactive(0.0)
    
    def on_mount(self) -> None:
        """Method to update the time to the current time."""
        
        self.set_interval(1, self.update_time)
        
    def update_time(self):
        """Method to update the time to the current time."""
        
        self.elapsed_time = monotonic() - self.start_time
    
    def watch_elapsed_time(self, elapsed_time: float) -> None:
        """Called when the time attribute changes."""
        
        minutes, seconds = divmod(elapsed_time, 60)
        
        self.update(f"{minutes:02.0f}:{seconds:02.0f}")