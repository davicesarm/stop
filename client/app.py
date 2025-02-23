from typing import Optional
from textual.app import App

# from textual.containers import VerticalScroll
from client.screens import Entry, Game, Ranking


class Potstop(App):  # type: ignore
    """Textual app to play Potstop"""

    CSS_PATH = "potstop.tcss"
    POTS = ['CEP', 'MSÉ', 'Ator', 'Nome', 'Música', 'Carro', 'Comida', 'Objeto', 'Verbo', 'Utensílio de cozinha']
    SCREENS = {"entry": Entry}
    PLAYERS = ['arthur - 21', 'mari - 19', 'cclaras - 14', 'davis - 13']

    def on_mount(self) -> None:
        self.theme = "dracula"
        
        def send_username_to_server(username: Optional[str]) -> None:
            
            #TODO: create send username to server logic here
            
            def send_pots_to_server(pots: Optional[list[str]]) -> None:
                
                self.push_screen(Ranking(game_leader=True, players=self.PLAYERS))

            assert username is not None
            self.sub_title = username
            self.push_screen(Game(pots=self.POTS), send_pots_to_server)
            self.notify(f"{username} entrou no jogo!")

        self.push_screen('entry', send_username_to_server)

if __name__ == "__main__":
    app = Potstop()
    app.run()
