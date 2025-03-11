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
        game_letter: str,
        on_stop: Callable[[dict[str, str]], None]
    ) -> None:
        super().__init__(id='game-screen')
        self.__pots = pots
        self.__game_letter = game_letter
        self.__on_stop = on_stop
        self.title = 'The letter is ' + game_letter

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            VerticalScroll(Horizontal(Button(self.__game_letter, id='letter-label', disabled=True), id='letter-horizontal'), *self.__gen_pots(), id="game-pots"),
            Horizontal(Timer(self.get_pots_and_dismiss), Button("POTS", classes="game-button"), id="game-horizontal"),
            id="game-main",
        )
        yield Footer()
        Button.press

    @on(Button.Pressed, '.game-button')
    def handle_game_stopped(self) -> None:
        if self.verify_pots():
            self.__on_stop(self.get_pots())
            
        
    def verify_pots(self):
        inputs = self.query(Input)
        invalids = 0
        first_invalid = None
        
        for _input in inputs:
            validated = _input.validate(_input.value)
            if validated and validated.failures:
                invalids += 1
                
                if not first_invalid:
                    first_invalid = _input.name
            
        if not invalids:
            return True
        else:
            self.notify(f"{first_invalid} and {invalids} other are invalid!")
            return False 
    
    def get_pots_and_dismiss(self):
        inputs = self.query(Input)
        answers: dict[str, str] = {}
        
        for _input in inputs:            
            assert isinstance(_input.name, str)
            answers[_input.name] = _input.value
            
        self.dismiss(answers)
    
    def get_pots(self):
        inputs = self.query(Input)
        answers: dict[str, str] = {}
        
        for _input in inputs:            
            assert isinstance(_input.name, str)
            answers[_input.name] = _input.value
        
        return answers

    def __gen_pots(self):
        for pot in self.__pots:
            inp = Input(name=pot, placeholder=pot, classes="pot", validators=Function(self.__validator, 'Value is not valid'))
            inp.tooltip = pot
            
            yield inp
            
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
                    