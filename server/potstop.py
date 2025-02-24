from data_structures.queue import Queue
from typing import Optional
import random
from collections import Counter

class Potstop:
    def __init__(self):
        # Pots padrão
        # self.__letter = self.gen_letter()
        self.__letter = "M"
        # self.__pots = ['CEP', 'MSÉ', 'Ator', 'Nome', 'Música', 'Carro', 'Comida', 'Objeto', 'Verbo', 'Utensílio de cozinha']
        self.__pots = ['Nome', "Cidade", "Comida", "Animal", "Objeto"]
        # {"Nome": "Mari", "Cidade": "Maragogi", "Comida": "Macaxeira", "Objeto": "Monitor"}
        self.__players = {}
        self.__order = Queue()
        self.__game_started = False
        self.__stopped = False
        self.stop_queue = Queue()
        self.answers = []
        self.__round = 0
        
    @property
    def stopped(self) -> bool:
        return self.__stopped

    def stop(self):
        self.__stopped = True

    @property
    def game_started(self) -> bool:
        return self.__game_started
    
    def start_game(self) -> None:
        self.__game_started = True

    def end_game(self) -> None:
        self.__game_started = False
        
    def get_players(self) -> list[str]:
        return list(self.__players.keys())
        
    def add_player_points(self, name: str, points: int) -> None:
        if name in self.__players:
            self.__players[name] += points
        
    def is_stop_valid(self, answer: dict) -> bool:
        for ans in answer.values():
            if len(ans) < 2 or ans[0].upper() != self.__letter.upper():
                return False
        return True
            
    def gen_letter(self) -> str:
        self.__letter = chr(random.randint(64, 90)).upper()
        return self.__letter
                
    def add_player(self, name: str, points: int = 0):
        self.__players[name] = points
        self.__order.enqueue(name)
        
    def remove_player(self, name: str) -> Optional[str]:
        if name not in self.__players:
            return None
        self.__order.remove(name)
        return self.__players.pop(name)
        
    def get_points(self, name: str) -> Optional[int]:
        return self.__players.get(name)
        
    def get_pots(self) -> list[str]:
        return self.__pots
    
    def remove_leader(self) -> Optional[str]:
        removed = self.__order.dequeue()
        if removed is not None:
            self.__players.pop(removed)
        return removed
        
    def get_leader(self) -> Optional[str]:
        return self.__order.peek()
    
    def get_ranking(self) -> dict:
        return dict(sorted(self.__players.items(), key=lambda i: i[1], reverse=1))
    
    def compute_points(self, name: str, answer: dict[str, str], counted_words: dict[str, dict[str, int]]) -> None:
        for category, ans in answer.items():
            try:
                if ans[0].upper() != self.__letter.upper():
                    continue
                
                if counted_words[category][ans] < 2:
                    self.add_player_points(name, 10)
                else:
                    self.add_player_points(name, 5)
            except KeyError:
                continue
    
    def count_words(self, answers: list[dict[str, str]]) -> dict[str, dict[str, int]]:
        """
        Conta quantas vezes cada resposta aparece por categoria.

        Args:
            answers: Lista de dicionários contendo as respostas dos jogadores.

        Returns:
            Um dicionário onde cada chave é uma categoria e o valor é outro dicionário com a contagem das respostas.
        """
        count = {}
        for pot in self.__pots:
            category = Counter()
            for ans in answers:
                value = ans.get(pot)
                if value is not None:
                    category[value] += 1
                    
            count[pot] = dict(category)
        return count
                
            
if __name__ == "__main__":   
    # Tests
    players = [
        ("arthur", 11),
        ("mari", 19),
        ("claras", 14),
        ("davis", 15)
    ]

    game = Potstop()
    for player in players:
        game.add_player(*player)

    print("---- Ranking ----")
    print("\n".join((f"{k} - {v}" for k,v in game.get_ranking().items())), end=" ")
    print("Ranking inicial\n")
    print(game.get_points("claras"), end=" ")
    print("Pontos de clara\n")
    print(game.get_leader(), end=" ")
    print("Lider\n")
    print(game.remove_leader(), end=" ")
    print("Tirando lider\n")
    game.add_player_points("davis", 5)
    print("Setando pontos de davis para 20\n")
    print("---- Ranking ----")
    print("\n".join((f"{k} - {v}" for k,v in game.get_ranking().items())), end=" ")
    print("Ranking atualizado\n")
    print(game.get_leader(), end=" ")
    print("Novo lider\n")

