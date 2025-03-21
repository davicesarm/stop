from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, ListView, ListItem, Label
from textual.containers import Horizontal, Vertical
from typing import Union


class Ranking(Screen[str]):
    """
    Ranking Screen
    This class represents a screen that displays the ranking of players in a game. It inherits from the `Screen` class
    and is designed to show a list of players along with their respective points, as well as provide buttons for restarting
    or quitting the game.
    
    Attributes:
        __players (list[list[Union[str, int]]]): A list of players where each player is represented as a list containing
            their name (str) and points (int).
    Methods:
        __init__(players: list[list[Union[str, int]]]) -> None:
            Initializes the Ranking screen with the given list of players.
        compose() -> ComposeResult:
            Composes the UI elements of the ranking screen, including the header, player ranking list, buttons, and footer.
        __gen_ranks():
            A generator function that yields list items for each player and their points to be displayed in the ranking list.
        handle_continue_game(event: Button.Pressed) -> None:
            Handles the event when a button is pressed. Dismisses the screen and returns the label of the pressed button
            in lowercase.
    """
    

    def __init__(self, players: list[list[Union[str, int]]]) -> None:
        super().__init__()
        self.__players = players

    def compose(self) -> ComposeResult:
        """
        Composes the UI components for the ranking screen.
        This method defines the structure and layout of the ranking screen by 
        yielding various UI elements, including a header, a vertical container 
        with a list view of ranks and buttons, and a footer.
        
        Yields:
            Header: The header component of the ranking screen.
            Vertical: A vertical container with a list view of ranks and buttons.
            Footer: The footer component of the ranking screen.
        """
        
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
        """
        Generates a sequence of ranking items based on player names and their points.
        Yields:
            ListItem: A list item containing a label with the player's name and points,
                      styled with the 'ranking-item' class.
        """
        
        for player, points in self.__players:
            yield ListItem(Label(f'{player} - {points}'), classes='ranking-item')

    @on(Button.Pressed)
    def handle_continue_game(self, event: Button.Pressed) -> None:
        """
        Handles the event triggered when a button is pressed.
        This method is called when a Button.Pressed event occurs. It dismisses
        the current screen or dialog and processes the button label associated
        with the event.
        Args:
            event (Button.Pressed): The event object containing information
                about the button press, including the button label.
        """
        
        self.dismiss(str(event.button.label).lower())
