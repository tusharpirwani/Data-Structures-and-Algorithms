# DSAListNode is the basic building block for the linked list
class DSAListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

# DSALinkedList manages the chain of nodes
class DSALinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None
    
    def insertFirst(self, value):
        newNode = DSAListNode(value)
        if self.isEmpty():
            # If the list is empty, the new node is both the head and the tail
            self.head = newNode
            self.tail = newNode
        else:
            self.head.prev = newNode # finds the current first node (self.head) and sets its .prev pointer to our new node
            newNode.next = self.head # it sets the new node's .next pointer to the current first node
            self.head = newNode # it updates the head pointer to the new node

    def insertLast(self, value):
        newNode = DSAListNode(value)
        if self.isEmpty():
            # If the list is empty, same as insertFirst
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail # The new node's 'prev' points to the old tail
            self.tail.next = newNode # Link the .next of old tail to the new node
            self.tail = newNode  # Update the tail to be the new node

    def peekFirst(self):
        if self.isEmpty():
            raise ValueError("Cannot peek at an empty list.")
        return self.head.value

    def peekLast(self):
        if self.isEmpty():
            raise ValueError("Cannot peek at an empty list.")
        return self.tail.value 

    def removeFirst(self):
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")
        
        removedValue = self.head.value # holds the value of first node in a temp variable 

        # This special case handles removing the last node from the list. It saves
        # the program from crashing because the logic in the 'else' block would
        # set self.head to None and then incorrectly try to access self.head.prev
        if self.head == self.tail: 
            self.head = None
            self.tail = None
        else:
            # Move head to the next node.
            self.head = self.head.next # changes the head from the first element to the next element(second)
            self.head.prev = None  # The new head's 'prev' must be set to None
            
        return removedValue                                

    def removeLast(self):
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")

        removedValue = self.tail.value

        # Special case for a single-item list
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev  # changes the tail from the last element to the second last element
            self.tail.next = None # The new tail's 'next' pointer must be set to None

        return removedValue
    
    def remove(self, value):
        """Removes a node with a specific value from the list."""
        if self.isEmpty():
            raise ValueError("Cannot remove from an empty list.")

        current_node = self.head
        while current_node is not None and current_node.value != value:
            current_node = current_node.next

        if current_node is None:
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




    def display(self, reverse=False):
        if self.isEmpty():
            print("List is empty.")
            return

        if not reverse:
            # Forward traversal
            currentNode = self.head
            print("HEAD -> ", end="")
            while currentNode is not None:
                print(f"[{currentNode.value}] -> ", end="")
                currentNode = currentNode.next
            print("None")
        else:
            # Reverse traversal using 'prev' pointers
            currentNode = self.tail
            print("None <- ", end="")
            while currentNode is not None:
                print(f"[{currentNode.value}] <- ", end="")
                currentNode = currentNode.prev
            print("TAIL")
