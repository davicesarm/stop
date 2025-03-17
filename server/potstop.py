from data_structures.queue import Queue
from data_structures.hashtable import HashTable
from typing import Optional
import random
from collections import Counter

class Potstop:
    """ 
    Class representing the Potstop game.
    
    **Public properties & attributes:**

    * answers: list[dict[str, str]] - List of player answers.
    * letter: str - Current letter.
    * pots: list[str] - Current categories.
    * player_limit: int - Player limit.
    * stopped: bool - Indicates if the game has been stopped.
    * game_started: bool - Indicates if the game has started.
    * players: list[str] - List of players.
    * leader: Optional[str] - Current leader.
    * ranking: list[tuple[str, int]] - Player ranking.
    * round: int - Current round.
    
    **Public methods:**
    
    * stop: None - Stops the game.
    * start_game: None - Starts the game.
    * end_game: None - Ends the game.
    * add_player_points: None - Adds points to a player.
    * is_stop_valid: bool - Checks if an answer is valid.
    * add_player: None - Adds a player.
    * remove_player: Optional[str] - Removes a player.
    * get_points: Optional[int] - Returns the points of a player.
    * remove_leader: Optional[str] - Removes the leader.
    * compute_points: None - Computes the points of a player.
    * count_words: dict[str, dict[str, int]] - Counts the words.
    """
    
    def __init__(self):
        import pots
        self.__avaliable_pots = pots.pots
        self.__pots = self.__gen_pots()
        self.__letter = self.__gen_letter()
        self.__player_limit = 8
        self.__players: HashTable[str, int] = HashTable()
        self.__order: Queue[str] = Queue()
        self.__game_started = False
        self.__stopped = False
        self.__round = 0
        self.answers: list[tuple[str, dict[str, str]]] = []
        
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
        """
        Stops the current game session.

        This method sets the stopped flag to True, indicating that the game
        has been stopped. It does not affect the game state or player data.
        """
        self.__stopped = True

    def start_game(self) -> None:
        """
        Starts a new game session.

        This method starts a new game session by generating new sets of
        categories and a letter. The game state is set to started, and 
        the round counter is incremented. Also, the answers list is cleared 
        and the stopped flag is set to False.
        """
        self.__gen_pots()
        self.__gen_letter()
        self.__round += 1
        self.__stopped = False
        self.answers.clear()
        self.__game_started = True

    def end_game(self) -> None:
        """
        Ends the current game session.

        This method sets the game state to not started, effectively ending
        the current game session. It should be called when the game needs
        to be terminated or completed, ensuring that the game status is
        updated accordingly.
        """

        self.__game_started = False
        
    def add_player_points(self, name: str, points: int) -> None:
        """
        Adds points to a player's score.

        Args:
            name: The name of the player to add points to.
            points: The number of points to add to the player's score.
        
        Returns:
            None
        """
        if name in self.__players:
            self.__players[name] += points
        
    def is_stop_valid(self, answer: str) -> bool:
        """
        Verifies if a given answer is valid.

        An answer is considered valid if:
        - It is longer than 2 characters.
        - It starts with the current game letter.
        - No character in the answer repeats more than twice.

        Args:
            answer: The answer string to validate.

        Returns:
            True if the answer is valid according to the criteria, otherwise False.
        """

        for i in range(len(answer)):
            qtd = 0
            for j in range(i, len(answer)):
                if qtd > 2:
                    return False
                if answer[i] == answer[j] and i != j:
                    qtd += 1
                    
        return len(answer) > 2 and answer[0].upper() == self.__letter.upper()
            
    def add_player(self, name: str, points: int = 0) -> None:
        """
        Adds a player to the game with an initial point value.

        This function registers a new player by adding their name to the players
        dictionary, initializing their score with the specified points. The player
        is also added to the order queue to track leaders by order.

        Args:
            name: The name of the player to be added.
            points: The initial score for the player. Defaults to 0.

        Returns:
            None
        """
        self.__players[name] = points
        self.__order.enqueue(name)
        
    def remove_player(self, name: str) -> Optional[str]:
        """
        Removes a player from the game.

        Removes a player from the game by deleting them from the players
        dictionary and the order queue. If the player is not found, the method
        returns None. If the player is removed and the game now has no players,
        the game is stopped.

        Args:
            name: The name of the player to be removed.

        Returns:
            The name of the removed player if they existed, otherwise None.
        """
        if name not in self.__players:
            return None
        self.__order.remove(name)
        removed = self.__players.remove(name)
        if len(self.__players) == 0:
            self.__game_started = False
        return removed
        
    def get_points(self, name: str) -> Optional[int]:
        """
        Gets the points for the player with the given name.

        Args:
            name: The name of the player to get the points for.

        Returns:
            The points for the player, or None if the player does not exist.
        """
        return self.__players.get(name)
        
    def remove_leader(self) -> Optional[str]:
        """
        Removes the leader from the game and returns their name.

        The leader is the player at the front of the order queue. If the queue
        is empty or the leader does not exist, the method returns None. The
        leader is removed from the order queue and the players dictionary.

        Returns:
            The name of the removed leader if they existed, otherwise None.
        """
        removed = self.__order.dequeue()
        if removed is not None:
            self.__players.remove(removed)
        return removed
        
    def compute_points(self, name: str, answer: dict[str, str], counted_words: dict[str, dict[str, int]]) -> None:
        """
        Computes and assigns points for a player's answers based on their uniqueness.

        This method evaluates each answer provided by a player in different categories.
        If an answer is valid and unique within its category, the player is awarded
        a higher point value. If the answer is not unique, a lower point value is assigned.
        Invalid answers are ignored.

        Args:
            name: The name of the player whose points are being computed.
            answer: A dictionary containing the player's answers, where each key is a category
                    and the value is the player's answer for that category.
            counted_words: A dictionary with categories as keys, and values being another
                        dictionary that counts how many times each answer appears across
                        all players.

        Returns:
            None
        """
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
        Counts the occurrences of each answer in given categories across all players.

        This method iterates through the list of player answers and counts how many
        times each answer appears for each category. The result is a dictionary where
        each key is a category, and the value is another dictionary representing the
        count of each answer within that category.

        Args:
            answers: A list of dictionaries containing player answers, where each key
                    is a category and the value is the player's answer for that category.

        Returns:
            A dictionary with categories as keys and values being dictionaries that map
            each answer to the count of its occurrences across all players.
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
        """
        Randomly generates a list of pot categories for the game.

        This method selects a random category from each available pot category
        set and assigns the resulting list to the instance variable `__pots`.

        Returns:
            A list of strings representing the randomly selected pot categories.
        """

        self.__pots = [random.choice(pot) for pot in self.__avaliable_pots]
        return self.__pots  
            
    def __gen_letter(self) -> str:
        """
        Randomly generates a letter for the game.

        The letter is selected from an alphabet where each letter has a weight
        associated with it. The weights are:
        - Common letters: 5
        - Rare letters (Z, X, Q, H, K, Y, W): 1 or 2

        The letter is then assigned to the instance variable `__letter`.

        Returns:
            A string representing the randomly selected letter.
        """
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
            
