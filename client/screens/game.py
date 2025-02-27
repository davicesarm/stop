from time import monotonic
from typing import Callable
from textual import on
from textual.screen import Screen
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Button, Header, Footer, Digits
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.validation import Function


class Game(Screen[dict[str, str]]):

    def __init__(
        self,
        pots: list[str],
        game_letter: str
    ) -> None:
        super().__init__()
        self.__pots = pots
        self.__game_letter = game_letter

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            VerticalScroll(*self.__gen_pots(), id="game-pots"),
            Horizontal(Timer(self.get_pots_and_dismiss), Button("POTS", classes="game-button"), id="game-horizontal"),
            id="game-main",
        )
        yield Footer()
        Button.press

    @on(Button.Pressed)
    def handle_game_stopped(self) -> None:
        self.get_pots_verify_and_dismiss()
        
    def get_pots_verify_and_dismiss(self):
        inputs = self.query(Input)
        answers: dict[str, str] = {}
        invalids = 0
        first_invalid = None
        
        for _input in inputs:
            validated = _input.validate(_input.value)
            if validated and validated.failures:
                invalids += 1
                
                if not first_invalid:
                    first_invalid = _input.name
            
            assert isinstance(_input.name, str)
            answers[_input.name] = _input.value
            
        if not invalids:
            self.dismiss(answers)
        else:
            self.notify(f"{first_invalid} and {invalids} other are invalid!")  
    
    def get_pots_and_dismiss(self):
        inputs = self.query(Input)
        answers: dict[str, str] = {}
        
        for _input in inputs:            
            assert isinstance(_input.name, str)
            answers[_input.name] = _input.value
            
        self.dismiss(answers)        

    def __gen_pots(self):
        for pot in self.__pots:
            yield Input(name=pot, placeholder=pot, classes="pot", validators=Function(self.__validator, 'Value is not valid'))
            
    def __validator(self, value: str) -> bool:
        if len(value) <= 2:
            return False
        
        if value[0].upper() != self.__game_letter:
            return False
        
        return True
            
            
            
class Timer(Digits):
    
    start_time: reactive[float] = reactive(monotonic)
    elapsed_time: reactive[float] = reactive(0.0)
    
    def __init__(self, stop: Callable[[], None]):
        super().__init__()
        self.target_time = 60*5
        self.__stop = stop
    
    def on_mount(self) -> None:
        """Method to update the time to the current time."""
        
        self.set_interval(1, self.update_time)
        
    def update_time(self):
        """Method to update the time to the current time."""
        
        self.elapsed_time = monotonic() - self.start_time
    
    def watch_elapsed_time(self, elapsed_time: float) -> None:
        """Called when the time attribute changes."""
        
        minutes, seconds = (self.target_time - int(elapsed_time)) // 60, (self.target_time - int(elapsed_time)) % 60
        self.update(f"{minutes}:{seconds:02}")
        
        if (self.target_time - int(self.elapsed_time)) < 0:
            self.__stop()
                    