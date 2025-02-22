from textual.app import App

# from textual.containers import VerticalScroll
from client.screens import Entry, Game


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"
    POTS = ['CEP', 'MSÉ', 'Ator', 'Nome', 'Música', 'Carro', 'Comida', 'Objeto', 'Verbo', 'Utensílio de cozinha']
    SCREENS = {"entry": Entry}

    def on_mount(self) -> None:
        self.theme = "dracula"
        
        def send_username_to_server(username: str | None) -> None:
            
            #TODO: create send username to server logic here

            assert username is not None
            self.sub_title = username
            self.push_screen(Game(pots=self.POTS))
            self.notify(f"{username} entrou no jogo!")

        self.push_screen('entry', send_username_to_server)

if __name__ == "__main__":
    app = Potstop()
    app.run()
