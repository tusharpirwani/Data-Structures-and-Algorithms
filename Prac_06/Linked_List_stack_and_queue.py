from Linked_List import DSALinkedList

class DSAStack:
    # Original array-based implementation from Practical 3, stacks and queue.

    def __init__(self):
        self.list = DSALinkedList()  # The stack uses a DSALinkedList object internally to store its data

    def push(self, value):
        """Adds an item to the top of the stack."""
        self.list.insertFirst(value) # By always inserting at the front of the list, we ensure the last
                                     # item added is the first one available (LIFO)

    def pop(self):
        """Removes and returns the item from the top of the stack."""
        return self.list.removeFirst()  # Removing from the front of the list ensures the last item pushed
                                        # is the first one to be removed

    def top(self):
        """Returns the top item of the stack without removing it."""
        return self.list.peekFirst()

    def is_empty(self):
        """Checks if the stack is empty."""
        return self.list.isEmpty()

class DSAQueue:
    # Original array-based implementation from Practical 3, stacks and queue.

    def __init__(self):
        self.list = DSALinkedList()

    def enqueue(self, value):
        """Adds an item to the rear of the queue."""
        self.list.insertLast(value) # To create a queue (FIFO), we add new items to the end of the list,
                                    # like a person joining the back of a line

    def dequeue(self):
        """Removes and returns the item from the front of the queue."""
        return self.list.removeFirst()  # We remove items from the front of the list, like serving the
                                        # first person in a line

    def peek(self):
        """Returns the front item of the queue without removing it."""
        return self.list.peekFirst()

    def is_empty(self):
        """Checks if the queue is empty."""
        return self.list.isEmpty()
    
if __name__ == "__main__":
 my_stack = DSAStack()
 print(f"Stack created. Is it empty? {my_stack.is_empty()}") 
 my_stack.push('A')

 print(f"Pushed 'A'. Top is now: {my_stack.top()}")
 my_stack.push('B')
 print(f"Pushed 'B'. Top is now: {my_stack.top()}")
 my_stack.push('C')
 print(f"Pushed 'C'. Top is now: {my_stack.top()}")

 popped_item = my_stack.pop() 
 print(f"Popped item: {popped_item}")
 print(f"Top is now: {my_stack.top()}") 

 popped_item = my_stack.pop()
 print(f"Popped item: {popped_item}") 
 print(f"Top is now: {my_stack.top()}") 

 my_queue = DSAQueue()
 print(f"Queue created. Is it empty? {my_queue.is_empty()}") 



 my_queue.enqueue(100)
 print(f"Enqueued 100. Front is: {my_queue.peek()}") 
 my_queue.enqueue(200)
 print(f"Enqueued 200. Front is still: {my_queue.peek()}") 
 my_queue.enqueue(300)
 print(f"Enqueued 300. Front is still: {my_queue.peek()}")
 print(f"Queue is now not empty. Is it empty? {my_queue.is_empty()}")



 dequeued_item = my_queue.dequeue() 
 print(f"Dequeued item: {dequeued_item}") 
 print(f"Front is now: {my_queue.peek()}") 

 dequeued_item = my_queue.dequeue()
 print(f"Dequeued item: {dequeued_item}") 
 print(f"Front is now: {my_queue.peek()}") 

 dequeued_item = my_queue.dequeue()
 print(f"Dequeued item: {dequeued_item}") 
 print(f"Queue is empty again. Is it empty? {my_queue.is_empty()}")

















