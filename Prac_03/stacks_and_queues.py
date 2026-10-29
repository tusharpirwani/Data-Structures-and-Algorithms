import numpy as np

class DSAStack:
    """Implements a LIFO (Last-In, First-Out) Stack data structure using a Python list as an array"""
    def __init__(self, capacity=100): # Initializes the stack with a fixed capacity
        self.stack = np.zeros(capacity, dtype=object) # The underlying array to store stack items
        self.count = 0                  # Tracks the number of items currently in the stack


    def get_count(self):
        """Returns the number of items in the stack"""
        return self.count
    
    def is_empty(self):
        """Checks if the stack is empty"""
        return self.count == 0
    
    def is_full(self):
        """Checks if the stack has reached its maximum capacity"""
        return self.count == len(self.stack) 
    
    def push(self, value):
         """Adds an item to the top of the stack"""
         if self.is_full():
            raise Exception("Stack overflow: Cannot push to a full stack.") # If the stack is full, raise an error to prevent an overflow
         else:
             # place the new value at the next empty spot
             # self.count always points to the next available index
             self.stack[self.count] = value
             self.count += 1   # Increment the count to reflect that a new item has been added

    def pop(self):
        """Removes and returns the item from the top of the stack"""
        if self.is_empty():
            raise Exception("Stack underflow: Cannot pop from an empty stack.")
        else:
            # The top item is at the index one less than the count
            top_item = self.stack[self.count - 1]
            self.count -= 1 # Logically remove the item by decrementing the count
            return top_item
    
    def top(self):
        """Returns the top item of the stack without removing it"""
        if self.is_empty():
            raise Exception("Stack is empty.")
        else:
            # The top item is at the index one less than the count
            return self.stack[self.count - 1]
        
# Queues (Parent & Children) 
class DSAQueue:
    """A base (parent) class for Queue implementations. Defines the common interface for all queues"""
    def __init__(self, capacity=100):
        self.queue = [None] * capacity
        self.count = 0

    def get_count(self):
        return self.count
     
    def is_empty(self):
        return self.count == 0
     
    def is_full(self):
        return self.count == len(self.queue)
    
    def enqueue(self, value):
       """Placeholder method: Subclasses must provide their own implementation"""
       raise NotImplementedError("Subclass must implement this method")

    def dequeue(self):
        raise NotImplementedError("Subclass must implement this method")

            
    def peek(self):
        raise NotImplementedError("Subclass must implement this method")

        
class DSAShufflingQueue(DSAQueue):
    """A simple but inefficient Queue that shuffles elements on dequeue"""
    def enqueue(self, value):
        """Adds an item to the rear of the queue."""
        if self.is_full():
            raise Exception("Queue is full.")
        else:
            self.queue[self.count] = value
            self.count += 1
    
    def dequeue(self):
        """Removes an item from the front and shuffles all other elements left"""
        if self.is_empty():
            raise Exception("Queue is empty.")
        else:
            front_item = self.queue[0] # Save the front item (at index 0)

            # Loop from the start to the second-to-last item
            # This shuffles all subsequent items one position to the left
            for  i in range (self.count - 1):
                self.queue[i] = self.queue[i + 1]

            # Decrement count and clear the duplicated last element
            self.count -= 1
            self.queue[self.count] = None

            # Return the item that was originally at the front
            return front_item 
    
    def peek(self):
        """Returns the front item, which is always at index 0"""
        if self.is_empty():
            raise Exception("Cannot peek at an empty queue.")
        else:
            return self.queue[0]
        
class DSACircularQueue(DSAQueue):
    
    def __init__(self, capacity=100):
        """Initializes the circular queue, including head and tail pointers"""
        super().__init__(capacity) # Call the parent class's constructor
        self.head = 0 # Pointer to the front of the queue
        self.tail = 0 # Pointer to the next empty spot at the rear
    
    
    def enqueue(self, value):
        """Adds an item to the tail of the queue, wrapping around if necessary"""
        if self.is_full():
            raise Exception("Queue is full.")
        else:
            self.queue[self.tail] = value
            self.tail = (self.tail + 1) % len(self.queue)  # Move the tail pointer, wrapping around to 0 if it reaches the end
            self.count += 1

    def dequeue(self):
        """Removes an item from the head of the queue, wrapping around if necessary"""
        if self.is_empty():
            raise Exception("Queue is empty.")
        else:
            front_item = self.queue[self.head]
            self.head = (self.head + 1) % len(self.queue) # Move the head pointer, wrapping around to 0 if it reaches the end
            self.count -= 1
            return front_item
        
    def peek(self):
        """Returns the front item, which is at the head pointer's position"""
        if self.is_empty():
            raise Exception("Cannot peek at an empty queue.")
        else:
            return self.queue[self.head]
        

def stack_menu():
    """An interactive menu to test the DSAStack class"""
    # Ask user for stack capacity, with error handling for invalid input
    try:
        size = int(input("Enter the desired capacity for the stack: "))
        stack = DSAStack(capacity=size)
    except ValueError:
        print("Invalid input, using default capacity of 100.")
        stack = DSAStack()

    # Using a boolean flag to control the menu loop
    is_running = True
    while is_running:
        print("\n--- Stack Menu ---")
        print("1. Push (add an item)")
        print("2. Pop (remove an item)")
        print("3. Top (peek at the top item)")
        print("4. View Count")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            value = input("Enter value to push: ")
            # Using try/except to gracefully handle errors from the stack class (e.g., overflow)
            try:
                stack.push(value)
                print(f"Pushed '{value}' onto the stack.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                value = stack.pop()
                print(f"Popped '{value}' from the stack.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                value = stack.top()
                print(f"The top item is '{value}'.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            print(f"The stack currently has {stack.get_count()} items.")
        elif choice == '5': # Set flag to False to exit the loop
            is_running = False
        else:
            print("Invalid choice, please try again.")

def queue_menu(queue_type):
    """An interactive menu to test a queue class."""
    if queue_type == 'shuffling':
        QueueClass = DSAShufflingQueue
        name = "Shuffling Queue"
    elif queue_type == 'circular':
        QueueClass = DSACircularQueue
        name = "Circular Queue"
    else:
        return
    
    # Ask user for queue capacity, with error handling
    try:
        size = int(input(f"Enter capacity for the {name}: "))
        queue = QueueClass(capacity=size)
    except ValueError:
        print("Invalid input, using default capacity of 100.")
        queue = QueueClass()

    is_running = True
    while is_running:
        print(f"\n--- {name} Menu ---")
        print("1. Enqueue (add an item)")
        print("2. Dequeue (remove an item)")
        print("3. Peek (view the front item)")
        print("4. View Count")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            value = input("Enter value to enqueue: ")
            try:
                queue.enqueue(value)
                print(f"Enqueued '{value}'.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                value = queue.dequeue()
                print(f"Dequeued '{value}'.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                value = queue.peek()
                print(f"The front item is '{value}'.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            print(f"The queue currently has {queue.get_count()} items.")
        elif choice == '5':
            is_running = False
        else:
            print("Invalid choice, please try again.")



# MAIN SCRIPT EXECUTION
# The 'if __name__ == "__main__"' block ensures this code only runs
# when the script is executed directly (not when imported as a module)
if __name__ == "__main__":
    # The main loop for the top-level menu
    is_running = True
    while is_running:
        print("\n--- Main Menu ---")
        print("Select the data structure to test:")
        print("1. Stack")
        print("2. Shuffling Queue")
        print("3. Circular Queue")
        print("4. Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == '1':
            stack_menu()
        elif main_choice == '2':
            queue_menu('shuffling')
        elif main_choice == '3':
            queue_menu('circular')
        elif main_choice == '4':
            print("Exiting program.")
            is_running = False # Set flag to False to exit the main loop
        else:
            print("Invalid choice, please select a valid option.")


 