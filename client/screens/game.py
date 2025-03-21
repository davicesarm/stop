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
    """
    Game Screen Class
    This class represents a game screen where players interact with a set of input fields (pots) 
    and a game letter. It provides functionality for validating user inputs, handling button 
    press events, and managing the game's lifecycle.
    Attributes:
        __pots (list[str]): A list of strings representing the names of the input fields (pots).
        __game_letter (str): The letter associated with the current game round.
        title (str): The title of the screen, indicating the current game letter.
    Methods:
        __init__(pots: list[str], game_letter: str) -> None:
            Initializes the Game screen with the provided pots and game letter.
        compose() -> ComposeResult:
            Composes the UI elements of the screen, including the header, footer, and main content.
        handle_game_stopped() -> None:
            Handles the event when the game button is pressed. Verifies the inputs and dismisses 
            the screen if all inputs are valid.
        verify_pots() -> bool:
            Validates all input fields (pots) and notifies the user if any are invalid.
        get_pots_and_dismiss() -> None:
            Retrieves the values of all input fields and dismisses the screen with the collected answers.
        get_pots() -> dict[str, str]:
            Collects the values of all input fields and returns them as a dictionary.
        __gen_pots() -> Generator[Input, None, None]:
            Generates input fields (pots) for the game screen based on the provided pot names.
        __validator(value: str) -> bool:
            Validates the input value based on the game's rules. Ensures the value starts with the 
            game letter and has a length greater than 2.
    """
    

    def __init__(
        self,
        pots: list[str],
        game_letter: str,
    ) -> None:
        super().__init__(id='game-screen')
        self.__pots = pots
        self.__game_letter = game_letter
        self.title = 'The letter is ' + game_letter

    def compose(self) -> ComposeResult:
        """
        Composes and yields the UI components for the game screen.
        This method defines the structure of the game screen by yielding
        various UI elements.

        Yields:
            Header: The header component of the game screen.
            Vertical: A vertical layout containing:
            - VerticalScroll: A scrollable horizontal section with:
                - Button: A disabled button displaying the game letter.
                - Dynamically generated input fields (pots).
            - Horizontal: A horizontal layout containing:
                - Timer: A timer widget to track the game's elapsed time.
                - Button: A button labeled "POTS" for game interaction.
            Footer: The footer component of the game screen.
        """
        
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
        """
        Handles the logic for when the game is stopped.
        This method checks if the conditions for verifying pots are met.
        If the conditions are satisfied, it retrieves the pots and dismisses
        the screen passing the data.
        Returns:
            None
        """
        
        if self.verify_pots():
            self.get_pots_and_dismiss()
            
        
    def verify_pots(self):
        """
        Validates all input pots and ensures they meet the required criteria.
        Iterates through the input fields, checks their validation status, and
        collects any invalid inputs. If invalid inputs are found, notifies the
        user with the name of the first invalid input and the total count.
        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
        
        inputs = self.query(Input)
        invalids: list[str] = []
        
        for _input in inputs:
            validated = _input.validate(_input.value)
            if validated and validated.failures:
                assert _input.name is not None
                invalids.append(_input.name)
            
        if not len(invalids):
            return True
        else:
            self.notify(f"{invalids[0]} and {invalids} other are invalid!")
            return False 
    
    def get_pots_and_dismiss(self):
        """
        Retrieves the pots (answers) and dismisses them.
        This method first calls `get_pots` to retrieve the answers, 
        then passes the retrieved answers to the `dismiss` method 
        for further processing.
        """
        
        answers = self.get_pots()
            
        self.dismiss(answers)
    
    def get_pots(self):
        """
        Retrieves a dictionary of input names and their corresponding values.
        This method queries all Input objects, validates that each input name is a string,
        and constructs a dictionary where the keys are input names and the values are 
        their associated input values.
        Returns:
            dict: A dictionary mapping input names to their values.
        """
        
        inputs = self.query(Input)
        answers: dict[str, str] = {}
        
        for _input in inputs:            
            assert isinstance(_input.name, str)
            answers[_input.name] = _input.value
        
        return answers

    def __gen_pots(self):
        """
        A generator method that creates and yields Input objects for each pot in the `__pots` attribute.
        Each Input object is initialized with:
        - `name`: The name of the pot.
        - `placeholder`: The name of the pot, used as a placeholder.
        - `classes`: A TCSS class named "pot".
        - `validators`: A validation function (`__validator`) with a custom error message.
        Additionally, a tooltip is set for each Input object using the pot's name.
        Yields:
            Input: An Input object configured for a specific pot.
        """
        
        for pot in self.__pots:
            inp = Input(name=pot, placeholder=pot, classes="pot", validators=Function(self.__validator, 'Value is not valid'))
            inp.tooltip = pot
            
            yield inp
            
    def __validator(self, value: str) -> bool:
        """
        Checks if the value has at least 2 characters and if the first letter corresponds to the game letter.
        Args:
            value (str): The string to be validated.
        Returns:
            bool: True if the string meets the following conditions:
                  - Its length is greater than 2.
                  - Its first character (case-insensitive) matches the game's letter.
                  Otherwise, returns False.
        """
        
        if len(value) < 2:
            return False
        
        if value[0].upper() != self.__game_letter:
            return False
        
        return True
            
            
            
class Timer(Digits):
    """
    Timer class that extends the Digits class to implement a countdown timer.
    Attributes:
        start_time (reactive[float]): A reactive attribute representing the start time of the timer.
        elapsed_time (reactive[float]): A reactive attribute representing the elapsed time since the timer started.
    Methods:
        __init__(stop: Callable[[], None]):
            Initializes the Timer instance with a target time and a stop callback function.
        on_mount() -> None:
            Sets up the timer to update every second after the component is mounted.
        update_time():
            Updates the elapsed time based on the current monotonic time.
        watch_elapsed_time(elapsed_time: float) -> None:
            Reactively updates the displayed time and stops the timer when the countdown reaches zero.
    """
    
    
    start_time: reactive[float] = reactive(monotonic)
    elapsed_time: reactive[float] = reactive(0.0)
    
    def __init__(self, stop: Callable[[], None]):
        super().__init__()
        self.target_time = 60*5
        self.__stop = stop
    
    def on_mount(self) -> None:
        """Mount event handler that set a periodic call to update_time."""
        
        self.set_interval(1, self.update_time)
        
    def update_time(self):
        """Update the time to the current time."""
        
        self.elapsed_time = monotonic() - self.start_time
        
        
    # watch is a textual "reserved" word to name functions that should watch reactive attributes
    def watch_elapsed_time(self, elapsed_time: float) -> None:
        """
        Monitors the elapsed time and updates the display accordingly.
        Args:
            elapsed_time (float): The amount of time that has elapsed in seconds.
        Behavior:
            - Calculates the remaining time by subtracting the elapsed time from the target time.
            - Updates the display with the remaining time in the format "MM:SS".
            - Stops the timer if the remaining time is less than zero.
        """
        """Called when the time attribute changes."""
        
        minutes, seconds = (self.target_time - int(elapsed_time)) // 60, (self.target_time - int(elapsed_time)) % 60
        self.update(f"{minutes}:{seconds:02}")
        
        if (self.target_time - int(self.elapsed_time)) < 0:
            self.__stop()
                    