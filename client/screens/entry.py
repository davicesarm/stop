from typing import Optional
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Input, Button, Header, Footer
from textual.containers import Vertical


class Entry(Screen[tuple[str, str]]):
    """
    Entry is a screen class that represents a user entry form for collecting a username and the server address.
    Attributes:
        __username (Optional[str]): The default username to pre-fill in the input field, if provided.
    Methods:
        __init__(username: Optional[str] = None):
            Initializes the Entry screen with an optional username.
        compose() -> ComposeResult:
            Constructs and yields the UI components for the screen, including a header, input fields for
            username and address, a button to submit the form, and a footer.
        handle_entry_sent() -> None:
            Handles the submission of the form when the user presses the button or submits the input.
            Validates the username and dismisses the screen with the collected username and address
            if valid. Otherwise, notifies the user of invalid input.
    """
    
    def __init__(self, username: Optional[str] = None):
        self.__username = username
        super().__init__()
        

    def compose(self) -> ComposeResult:
        """
        Composes the UI components for the entry screen.
        This method defines the structure and layout of the entry screen by yielding
        various UI elements such as a header, input fields, a button, and a footer.
        Yields:
            Header: The header component of the entry screen.
            Vertical: A vertical container holding the following components:
                - Input: An input field for the user's name with a placeholder "Seu nome".
                - Input: An input field for the server address with a placeholder "192.168.0.1:8888".
                - Button: A button labeled "Entrar".
            Footer: The footer component of the entry screen.
        """
        
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
        """
        Handles the submission of entry data from the user interface.
        This method retrieves the values of the 'name' and 'address' input fields
        from the user interface. It validates the 'name' field to ensure it is not
        empty. If the 'name' field is empty, a notification is displayed to inform
        the user of the invalid input. Otherwise, the method processes the input
        by stripping any leading or trailing whitespace and dismisses the current
        view with the processed data.
        Returns:
            None
        """
        
        name = self.query_one('#entry-name', Input)
        address = self.query_one('#entry-address', Input)        
        
        if name.value == '':
            self.notify('Invalid username: empty!')
        else:
            self.dismiss((name.value.strip(), address.value.strip()))
