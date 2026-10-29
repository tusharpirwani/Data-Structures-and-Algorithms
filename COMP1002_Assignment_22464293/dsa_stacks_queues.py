
# =================================================================
# File: dsa_stacks_queues.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Provides reusable Stack and Queue implementations,
#          utilizing the DSALinkedList.
#          Based on concepts covered in Practical 4.
# =================================================================

from dsa_linked_list import DSALinkedList

class DSAStack:
    """A Stack implementation using a Linked List."""
    def __init__(self):
        self.list = DSALinkedList()

    def push(self, value):
        """Adds an item to the top of the stack."""
        self.list.insertFirst(value)

    def pop(self):
        """Removes and returns the item from the top of the stack."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self.list.removeFirst()

    def top(self):
        """Returns the top item of the stack without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self.list.peekFirst()

    def is_empty(self):
        """Checks if the stack is empty."""
        return self.list.isEmpty()

class DSAQueue:
    """A Queue implementation using a Linked List."""
    def __init__(self):
        self.list = DSALinkedList()

    def enqueue(self, value):
        """Adds an item to the rear of the queue."""
        self.list.insertLast(value)

    def dequeue(self):
        """Removes and returns the item from the front of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        return self.list.removeFirst()

    def peek(self):
        """Returns the front item of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")
        return self.list.peekFirst()

    def is_empty(self):
        """Checks if the queue is empty."""
        return self.list.isEmpty()