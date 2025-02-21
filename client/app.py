from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input

# from textual.containers import VerticalScroll
from screens.entry import Entry
import unicodedata


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"
    SCREENS = {"entry": Entry}

    def on_mount(self) -> None:
        self.theme = "dracula"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        def send_username_to_server(username: str | None) -> None:
            self.notify(f"Username: {username}")

            assert username is not None
            self.sub_title = username
            self.push_screen("entry", send_username_to_server)

        self.push_screen("entry", send_username_to_server)
        # yield VerticalScroll(*self.gen_pots(['CEP', 'MSÉ', 'Ator']),
        #     id="grid",
        # )

    def gen_pots(self, pots: list[str]):
        for pot in pots:
            yield Input(id=self.normalize(pot.lower()), placeholder=pot, classes="pots")

    def normalize(self, s: str) -> str:
        """
        Normalize a string by removing diacritics.

        Args:
            s (str): The input string to normalize.

        Returns:
            str: The normalized string with diacritics removed.
        """
        # Normalize the string to NFD form (decomposed)
        decomposed = unicodedata.normalize("NFD", s)
        # Remove the diacritical marks (combining characters)
        normalized = "".join(c for c in decomposed if not unicodedata.combining(c))
        return normalized


if __name__ == "__main__":
    app = Potstop()
    app.run()
