from data_structures.queue import Queue
from data_structures.hashtable import HashTable
from typing import Optional
import random
from collections import Counter

class Potstop:
    def __init__(self):
        from pots import pots
        self.__avaliable_pots = pots
        self.__pots = self.__gen_pots()
        self.__letter = self.__gen_letter()
        self.__player_limit = 8
        self.__players = HashTable()
        self.__order = Queue()
        self.__game_started = False
        self.__stopped = False
        self.__round = 0
        self.answers = []
        
    @property
    def letter(self) -> str:
        return self.__letter
        
    @property
    def pots(self) -> list[str]:
        return self.__pots
        
    @property
    def player_limit(self) -> int:
        return self.__player_limit
    
    @player_limit.setter
    def player_limit(self, limit: int) -> None:
        if limit > 1:
            self.__player_limit = limit
        
    @property
    def stopped(self) -> bool:
        return self.__stopped

    @property
    def game_started(self) -> bool:
        return self.__game_started
    
    @property
    def players(self) -> list[str]:
        return self.__players.keys()
    
    @property
    def leader(self) -> Optional[str]:
        return self.__order.peek()
    
    @property
    def ranking(self) -> list[tuple[str, int]]:
        return sorted(self.__players.items(), key=lambda i: i[1], reverse=1)
    
    @property
    def round(self):
        return self.__round
    
    def stop(self):
        self.__stopped = True

    def start_game(self) -> None:
        self.__gen_pots()
        self.__gen_letter()
        self.__round += 1
        self.__stopped = False
        self.answers.clear()
        self.__game_started = True

    def end_game(self) -> None:
        self.__game_started = False
        
    def add_player_points(self, name: str, points: int) -> None:
        if name in self.__players:
            self.__players[name] += points
        
    def is_stop_valid(self, answer: str) -> bool:
        for i in range(len(answer)):
            qtd = 0
            for j in range(i, len(answer)):
                if qtd > 2:
                    return False
                if answer[i] == answer[j] and i != j:
                    qtd += 1
                    
        return len(answer) > 2 and answer[0].upper() == self.__letter.upper()
            
    def add_player(self, name: str, points: int = 0):
        self.__players[name] = points
        self.__order.enqueue(name)
        
    def remove_player(self, name: str) -> Optional[str]:
        if name not in self.__players:
            return None
        self.__order.remove(name)
        removed = self.__players.remove(name)
        if len(self.__players) == 0:
            self.__game_started = False
        return removed
        
    def get_points(self, name: str) -> Optional[int]:
        return self.__players.get(name)
        
    def remove_leader(self) -> Optional[str]:
        removed = self.__order.dequeue()
        if removed is not None:
            self.__players.remove(removed)
        return removed
        
    def compute_points(self, name: str, answer: dict[str, str], counted_words: dict[str, dict[str, int]]) -> None:
        for category, ans in answer.items():
            try:
                if not self.is_stop_valid(ans):
                    continue
                
                if counted_words[category][ans] == 1:
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
              
    def __gen_pots(self) -> list[str]:
        self.__pots = [random.choice(pot) for pot in self.__avaliable_pots]
        return self.__pots  
            
    def __gen_letter(self) -> str:
        self.letters = [chr(i) for i in range(65, 91)]
        self.weights = [5] * 26
        rare = (
            ("Z", 1), ("X", 1), ("Q", 2),
            ("H", 2), ("K", 2), ("Y", 1),
            ("W", 1)
        )
        for letter, weight in rare:
            self.weights[ord(letter) - 65] = weight
        self.__letter = random.choices(self.letters, weights=self.weights, k=1)[0]
        return self.__letter
            
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
    print("\n".join((f"{k} - {v}" for k,v in game.ranking)), end=" ")
    print("Ranking inicial\n")
    print(game.get_points("claras"), end=" ")
    print("Pontos de clara\n")
    print(game.leader, end=" ")
    print("Lider\n")
    print(game.remove_leader(), end=" ")
    print("Tirando lider\n")
    game.add_player_points("davis", 5)
    print("Setando pontos de davis para 20\n")
    print("---- Ranking ----")
    print("\n".join((f"{k} - {v}" for k,v in game.ranking)), end=" ")
    print("Ranking atualizado\n")
    print(game.leader, end=" ")
    print("Novo lider\n")

