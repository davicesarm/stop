from data_structures.queue import Queue
import heapq as heap

class Potstop:
    def __init__(self):
        self.__pots = ['CEP', 'MSÉ', 'Ator']
        self.__players = Queue()
        self.__ranking = heap.heapify([])
        self.__round = 0

