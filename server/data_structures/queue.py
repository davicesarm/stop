from typing import Any

class Node:
    def __init__(self, value: Any):
        self.value = value
        self.next = None    
    
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def __len__(self) -> int:
        return self.size
        
    def peek(self) -> Any:
        return self.head.value
        
    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0
        
    def enqueue(self, value) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        
    def dequeue(self) -> Any:
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self.size += 1
        return value
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def remove(self, key):
        current = self.head
        previous = None
        while current:
            if current.value == key:
                if previous:  
                    previous.next = current.next
                else:  
                    self.head = current.next
                if current == self.tail: 
                    self.tail = previous
                return current.value  
            previous = current
            current = current.next
        
        return None

    def __contains__(self, value) -> bool:
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False
    
    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next
            
    def __str__(self) -> str:
        return str([value for value in self])
    
        
    