class Node:
    def __init__(self, value):
        self.value = value
        self.next = None    
    
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def __len__(self):
        return self.size
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        
    def dequeue(self):
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self.size += 1
        return value
    
    def is_empty(self):
        return self.size == 0
    
    def __contains__(self, value):
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
            
    def __str__(self):
        return str([value for value in self])
    
        
    