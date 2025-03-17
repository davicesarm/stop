from typing import Any

class Node:
    def __init__(self, value: Any):
        self.value = value
        self.next = None    
    
class Queue:
    """
    A Queue data structure, implemented as a linked list.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def __len__(self) -> int:
        """
        Returns the size of the queue.
        """
        return self.size
        
    def peek(self) -> Any:
        """
        Returns the value of the front of the queue.
        """
        return self.head.value
        
    def clear(self) -> None:
        """
        Clears the queue.
        """
        self.head = None
        self.tail = None
        self.size = 0
        
    def enqueue(self, value) -> None:
        """
        Adds a value to the back of the queue.
        """
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        
    def dequeue(self) -> Any:
        """
        Removes the value from the front of the queue and returns it.
        """
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self.size += 1
        return value
    
    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        """
        return self.size == 0
    
    def remove(self, key):
        """
        Removes the first occurrence of a value in the queue.
        """
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
        """
        Checks if a value is in the queue.
        """
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False
    
    def __iter__(self):
        """
        Returns an iterator for the queue.
        """
        current = self.head
        while current is not None:
            yield current.value
            current = current.next
            
    def __str__(self) -> str:
        """
        Returns a string representation of the queue.
        """
        return str([value for value in self])
    
        
    