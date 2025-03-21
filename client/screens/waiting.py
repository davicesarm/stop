from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, LoadingIndicator, Button, Label
from textual.containers import Vertical


class Waiting(Screen): #type: ignore
    """
    Waiting Screen
    This class represents a screen that displays a waiting interface for a Potstop lobby. 
    It provides visual feedback to the user while waiting for the game to start or 
    indicates if the lobby is full.
    Attributes:
        __full_lobby (bool): A flag indicating whether the lobby is full. Defaults to False.
    Methods:
        __init__(full_lobby: bool = False):
            Initializes the Waiting screen with an optional full_lobby flag.
        compose() -> ComposeResult:
            Composes the UI elements of the screen, including a header, a loading indicator, 
            a button or label depending on the lobby state, and a footer.
        handle_game_start() -> None:
            Handles the event when the "Start game!" button is pressed, dismissing the screen.
    """
    
    
    def __init__(self, full_lobby: bool = False):
        super().__init__()
        self.__full_lobby = full_lobby

    def compose(self) -> ComposeResult:
        """
        Composes the UI components for the waiting screen.
        This method defines the structure of the waiting screen by yielding
        various UI elements such as a header, a vertical container with a
        loading indicator and either a button or a label (depending on the
        lobby state), and a footer.
        Yields:
            Header: The header component of the screen.
            Vertical: A vertical container holding the loading indicator and
                      either a button or a label.
            Footer: The footer component of the screen.
        """
        
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
        """
        Handles the start of the game by dismissing the current screen.
        This method is triggered when the button is pressed and ensures that the 
        appropriate UI elements are updated or closed.
        Returns:
            None
        """
        
        self.dismiss() #type: ignore