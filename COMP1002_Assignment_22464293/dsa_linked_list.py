# =================================================================
# File: dsa_linked_list.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Provides a reusable Doubly Linked List implementation.
#          Based on concepts covered in Practical 4.
# =================================================================

class DSAListNode:
    """A node for a doubly-linked list."""
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DSALinkedList:
    """A doubly-linked list implementation."""
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        """Checks if the list is empty."""
        return self.head is None
    
    def insertFirst(self, value):
        """Inserts a new value at the head of the list."""
        newNode = DSAListNode(value)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            self.head.prev = newNode
            newNode.next = self.head
            self.head = newNode

    def insertLast(self, value):
        """Inserts a new value at the tail of the list."""
        newNode = DSAListNode(value)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

    def peekFirst(self):
        """Returns the value at the head without removing it."""
        if self.isEmpty():
            raise ValueError("Cannot peek at an empty list.")
        return self.head.value

    def peekLast(self):
        """Returns the value at the tail without removing it."""
        if self.isEmpty():
            raise ValueError("Cannot peek at an empty list.")
        return self.tail.value 

    def removeFirst(self):
        """Removes and returns the value from the head of the list."""
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")
        
        removedValue = self.head.value

        if self.head == self.tail: 
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            
        return removedValue                                

    def removeLast(self):
        """Removes and returns the value from the tail of the list."""
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")

        removedValue = self.tail.value

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        return removedValue
    
    def remove(self, value):
        """Removes a node with a specific value from the list."""
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")

        current_node = self.head
        found = False
        while current_node is not None and not found:
             # Check if the values match 
             if current_node.value == value:
                 found = True
             else:
                current_node = current_node.next

        if current_node is None: # Value was not found
            raise ValueError("Value not found in list.")
        
        # If the node to remove is the head or tail, use existing methods
        if current_node == self.head:
            self.removeFirst()
        elif current_node == self.tail:
            self.removeLast()
        else:
            # Bypass the node
            current_node.prev.next = current_node.next
            current_node.next.prev = current_node.prev