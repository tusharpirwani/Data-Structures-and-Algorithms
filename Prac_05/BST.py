# Represents a single node in the doubly linked list.
class DSAListNode:
    def __init__(self, value):
        self.value = value  # The data stored in the node
        self.next = None    # Reference to the next node in the list
        self.prev = None    # Reference to the previous node in the list

# Manages the collection of DSAListNode objects.
class DSALinkedList:
    def __init__(self):
        # The list starts empty, so head and tail point to nothing.
        self.head = None
        self.tail = None

    # Checks if the list has any nodes.
    def isEmpty(self):
        return self.head is None
    
    # Adds a new node with the given value to the end of the list.
    def insertLast(self, value):
        newNode = DSAListNode(value)
        if self.isEmpty():
            # If the list is empty, the new node is both the first and last node.
            self.head = newNode
            self.tail = newNode
        else:
            # Link the new node after the current tail.
            newNode.prev = self.tail
            self.tail.next = newNode
            # Update the tail to be the new node.
            self.tail = newNode

    # Prints the contents of the list from head to tail.
    def display(self):
        if self.isEmpty():
            print("List is empty.")
            return

        # Start at the beginning of the list.
        currentNode = self.head
        print("HEAD -> ", end="")
        # Loop until we reach the end of the list.
        while currentNode is not None: # Loops as long as currentNode is not None (i.e., we haven't reached the end).
            print(f"[{currentNode.value}] -> ", end="")  # Prints the value of the current node.
            # Move to the next node.
            currentNode = currentNode.next
        print("None") # Prints the final part of the display string.


# Represents a single node in the binary search tree.
class DSATreeNode:
    def __init__(self, inKey, inValue):
        self.key = inKey      # The key used for sorting and searching
        self.value = inValue  # The data associated with the key
        self.left = None      # Reference to the left child node (smaller keys)
        self.right = None     # Reference to the right child node (larger keys)

# Manages the collection of DSATreeNode objects.
class DSABinarySearchTree:
    def __init__(self):
        # The tree starts empty with no root node.
        self.root = None

   

    # Public method that users call to find a key. It starts the search from the root.
    def find(self, key):
        return self._findRec(key, self.root)  # Calls the private recursive helper function, starting from the root.

    # Private method that performs the recursive search.
    def _findRec(self, key, currentNode):
        value = None # Initializes the return value to None.
        if currentNode is None:
            # Base Case 1: If we reach a null spot, the key doesn't exist.
            raise ValueError("Key " + str(key) + " not found")
        elif key == currentNode.key:
            # Base Case 2: We found the key, return its value.
            value = currentNode.value
        elif key < currentNode.key:
            # Recursive Step: The key is smaller, so search in the left subtree.
            value = self._findRec(key, currentNode.left)
        else:
            # Recursive Step: The key is larger, so search in the right subtree.
            value = self._findRec(key, currentNode.right)
        return value

    # Public method to insert a new node. It starts the process at the root.
    def insert(self, key, value):
        self.root = self._insertRec(key, value, self.root) # Calls the recursive helper and updates the root with the returned tree structure.

    # Private method that recursively finds the correct spot to insert a new node.
    def _insertRec(self, key, value, currentNode):
        updateNode = currentNode
        if currentNode is None:
            # Base Case: We've found an empty spot, so create the new node here.
            newNode = DSATreeNode(key, value)
            updateNode = newNode
        elif key < currentNode.key:  # Recursive step: If the new key is smaller than the current node's key.
            currentNode.left = self._insertRec(key, value, currentNode.left) # Call this function on the left child and update the left link.
        elif key > currentNode.key:  # Recursive step: If the new key is larger than the current node's key.
            currentNode.right = self._insertRec(key, value, currentNode.right)  # Call this function on the right child and update the right link.
        else:
            # If the key already exists, we cannot insert a duplicate.
            raise ValueError("Key already exists in the tree.")
        return updateNode

    # Public method to delete a node by its key.
    def delete(self, key):
        self.root = self._deleteRec(key, self.root) # Calls the recursive helper and updates the root with the returned tree structure.

    # Private method that recursively finds and deletes a node.
    def _deleteRec(self, key, currentNode):
        updateNode = currentNode
        # If the current node is None, the key was not found.
        if currentNode is None:
            raise ValueError("Key " + str(key) + " not found")
        # Recursive step: If the key is smaller, go left.
        elif key < currentNode.key:
            currentNode.left = self._deleteRec(key, currentNode.left)
        # Recursive step: If the key is larger, go right.
        elif key > currentNode.key:
            currentNode.right = self._deleteRec(key, currentNode.right)
         # If we are here, we have found the node to delete.
        else: 
            # Case 1: The node is a leaf (no children). Simply remove it.
            if currentNode.left is None and currentNode.right is None:
                updateNode = None  # The node to return is None, effectively deleting it.
            # Case 2: The node has one child. Replace the node with its child.
            elif currentNode.left is not None and currentNode.right is None:
                # The left child is promoted to take this node's place.
                updateNode = currentNode.left
            elif currentNode.left is None and currentNode.right is not None:
                # The right child is promoted to take this node's place.
                updateNode = currentNode.right
            # Case 3: The node has two children
            else:
                # Find the successor (the smallest node in the right subtree).
                successor = self._getMin(currentNode.right)
                # Copy the successor's data to the current node.
                currentNode.key = successor.key
                currentNode.value = successor.value
                # Recursively delete the original successor node from the right subtree.
                currentNode.right = self._deleteRec(successor.key, currentNode.right)
        return updateNode # Return the updated node structure.

    # Helper function to find the minimum node in a given subtree (by going left repeatedly).
    def _getMin(self, currentNode):
        # Keep traveling left until there are no more left children.
        while currentNode.left is not None:
             # Move to the left child.
            currentNode = currentNode.left
        return currentNode  # Return the leftmost node.

    
    # Finds the smallest key in the entire tree.
    def min(self):
        # Raise an error if the tree is empty.
        if self.root is None: raise ValueError("Tree is empty")
        # Call the helper function starting from the root and return its key.
        return self._getMin(self.root).key 

    # Finds the largest key in the entire tree (by going right repeatedly).
    def max(self):
        if self.root is None: raise ValueError("Tree is empty")  # Raise an error if the tree is empty.
        currentNode = self.root # Start at the root.
        while currentNode.right is not None:  # Keep traveling right until there are no more right children.
            currentNode = currentNode.right  # Move to the right child.
        return currentNode.key  # Return the rightmost node's key.

    # Public method to get the height of the tree.
    def height(self):
        return self._heightRec(self.root) # Calls the recursive helper, starting from the root.

    # Private recursive method to calculate the height.
    def _heightRec(self, currentNode):
        if currentNode is None:
            # Base Case: An empty tree or null spot has a height of -1.
            h = -1
        # If the node exists:
        else:
            # Recursively find the height of the left and right subtrees.
            leftHeight = self._heightRec(currentNode.left)
            rightHeight = self._heightRec(currentNode.right)
            # The height is 1 plus the height of the taller subtree.
            h = 1 + max(leftHeight, rightHeight)
        return h  # Return the calculated height.

    # Calculates a balance score based on the heights of the root's subtrees.
    def balance(self):
        # An empty tree is considered 100% balanced.
        if self.root is None: return 100.0
        leftHeight = self._heightRec(self.root.left) # Get the height of the left subtree of the root.
        rightHeight = self._heightRec(self.root.right) # Get the height of the right subtree of the root.
        treeHeight = self.height() # Get the total height of the tree
        if treeHeight < 1: return 100.0  # A single-node tree is 100% balanced.
        height_diff = abs(leftHeight - rightHeight)  # Calculate the absolute difference in heights.
        balance_factor = 1.0 - (height_diff / treeHeight) # Calculate the balance factor (1.0 is perfect, closer to 0 is worse).
        return balance_factor * 100  # Return the result as a percentage.

    
    # In-order traversal (Left, Node, Right). Returns keys in sorted order.
    def inorder(self):
        traversed_list = DSALinkedList() # Create a new empty linked list to store the results.
        self._inorderRec(self.root, traversed_list)  # Call the recursive helper to populate the list.
        return traversed_list 

    def _inorderRec(self, currentNode, linked_list):
        # Base case: do nothing if the node is None.
        if currentNode is not None:
            self._inorderRec(currentNode.left, linked_list) # 1. Traverse the left subtree.
            linked_list.insertLast(currentNode.key) # 2. Visit the node (add its key to the list).
            self._inorderRec(currentNode.right, linked_list)  # 3. Traverse the right subtree.

    # Pre-order traversal (Node, Left, Right). Useful for copying a tree.
    def preorder(self):
        traversed_list = DSALinkedList()
        self._preorderRec(self.root, traversed_list)
        return traversed_list

    def _preorderRec(self, currentNode, linked_list):
        # Base case: do nothing if the node is None.
        if currentNode is not None:
            linked_list.insertLast(currentNode.key) # 1. Visit the node (add its key to the list).
            self._preorderRec(currentNode.left, linked_list)  # 2. Traverse the left subtree.
            self._preorderRec(currentNode.right, linked_list)  # 2. Traverse the right subtree.

    # Post-order traversal (Left, Right, Node).
    def postorder(self):
        traversed_list = DSALinkedList()
        self._postorderRec(self.root, traversed_list)
        return traversed_list

    def _postorderRec(self, currentNode, linked_list):
        # Base case: do nothing if the node is None
        if currentNode is not None:
            self._postorderRec(currentNode.left, linked_list) # 2. Traverse the left subtree.
            self._postorderRec(currentNode.right, linked_list) # 2. Traverse the right subtree.
            linked_list.insertLast(currentNode.key) # 1. Visit the node (add its key to the list).


# This block runs only when the script is executed directly.
if __name__ == "__main__":
    # Create an instance of our tree.
    bst = DSABinarySearchTree()  # Creates a new, empty binary search tree object.
    choice = 0  # Initializes the choice variable to start the menu loop.
    # The main loop for the menu. It continues until the user chooses to exit.
    while choice != 7:
        print("\n--- Tree Menu ---")
        print("1. Add Node")
        print("2. Display Tree")
        print("3. Find Node")
        print("4. Delete Node")
        print("5. Get Stats (Min/Max, Height, Balance)")
        print("7. Exit")
        
        try:
            # Read user's choice.
            choice_str = input("Enter your choice (1-7): ") # Prompts the user for their choice and reads it as a string.
            if choice_str:  # If the user entered something:
                choice = int(choice_str)  # Convert the string to an integer.
            else: # If the user just pressed Enter:
                # Skip the rest of the loop and show the menu again.
                continue

            # Call the appropriate method based on the user's choice.
            if choice == 1:
                # Prompt for the key.
                key_str = input("Enter the key (integer): ")
                # Convert the key to an integer.
                key = int(key_str)
                # Use the key's string form as the value for simplicity.
                value = key_str 
                # Call the insert method to add the new node.
                bst.insert(key, value)
                print(f"Node '{key}' added.")
            elif choice == 2:
                # Check if the tree is empty first.
                if bst.root is None:
                    print("Tree is empty.")
                else:
                     # Ask the user which traversal they want to see.
                    display_choice = input("Choose traversal (inorder, preorder, postorder): ").lower()
                     # Call the appropriate traversal method based on input.
                    if display_choice == "inorder": bst.inorder().display()
                    elif display_choice == "preorder": bst.preorder().display()
                    elif display_choice == "postorder": bst.postorder().display()
                    else: print("Invalid traversal type.")   # Handle invalid traversal choices.
            elif choice == 3:
                key = int(input("Enter key to find: "))  # Prompt for the key to find.
                value = bst.find(key)  # Call the find method.
                print(f"Found value: '{value}' for key '{key}'.")
            elif choice == 4:
                key = int(input("Enter key to delete: ")) # Prompt for the key to delete.
                bst.delete(key)    # Call the delete method.
                print(f"Node with key '{key}' deleted.")
            elif choice == 5:
                if bst.root is None: raise ValueError("Tree is empty") # Check if the tree is empty to avoid errors.
                 # Print all the calculated statistics.
                print(f"Minimum key: {bst.min()}")
                print(f"Maximum key: {bst.max()}")
                print(f"Tree height: {bst.height()}")
                print(f"Balance score: {bst.balance():.2f}%")
            elif choice == 7:
                print("Exiting.")
            else:
                    print("Invalid choice.")
        # Catch errors to prevent the program from crashing on bad input.
        except ValueError as e:
            print(f"\nError: {e}. Please try again.")
        except TypeError:
            print("\nError: Invalid input. Please enter numbers for keys and choices.")