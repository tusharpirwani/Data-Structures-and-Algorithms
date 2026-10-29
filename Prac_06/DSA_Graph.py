from Linked_List import DSALinkedList
from Linked_List_stack_and_queue import DSAStack, DSAQueue

class DSAGraphNode:
    """Represents a single vertex (node) in the graph."""
    def __init__(self, p_label):
        """Constructor for a DSAGraphNode."""
        self._label = p_label  # The unique identifier for the node (e.g., 'A').
        self._links = DSALinkedList()  # This node's adjacency list, storing its neighbors.
        self._visited = False  # A flag used by traversal algorithms.

    def get_label(self):
        """Returns the label of the node."""
        return self._label
    
    def get_adjacent(self):
        """Returns the linked list of adjacent nodes."""
        return self._links

    def add_edge(self, vertex):
        """Adds a connection from this node to another vertex."""
        self._links.insertLast(vertex)

    def remove_edge(self, vertex):
        """Removes a connection from this node to another vertex."""
        self._links.remove(vertex)

    def set_visited(self):
        """Marks the node as visited."""
        self._visited = True

    def clear_visited(self):
        """Resets the visited flag to False."""
        self._visited = False
    
    def get_visited(self):
        """Checks if the node has been visited."""
        return self._visited
        
    def _sort_neighbors(self, temp_list):
        """
        Sorts a temporary list of neighbor nodes using the bubble sort logic (from Prac01).
        This ensures traversals are consistent.
        """
        n = 0
        for item in temp_list: n += 1  # Get the length of the list.
        for i in range(n):
            for j in range(0, n - i - 1):
                # Compare nodes based on their string labels.
                if temp_list[j].get_label() > temp_list[j+1].get_label():
                    # Perform the swap.
                    temp_list[j], temp_list[j+1] = temp_list[j+1], temp_list[j]
        return temp_list

    def get_adjacent_sorted(self):
        """
        Returns a sorted Python list of adjacent nodes.
        This is a helper for the traversal algorithms.
        """
        adj_list = []  # A temporary Python list to hold neighbors for sorting.
        current_node = self._links.head # Start at the beginning (the head) of this node's adjacency list (_links).
        while current_node is not None:  # Loop as long as we have not reached the end of the adjacency list.
            adj_list.append(current_node.value) # Add the actual neighbor node object to our temporary list.
            current_node = current_node.next  # Move to the next neighbor in the adjacency list.
        return self._sort_neighbors(adj_list)  # Call the custom sort method.

    def __str__(self):
        """Returns the string representation of the node (its label)."""
        return str(self._label)

# =================================================================
# DSAGraph Class Definition
# =================================================================
class DSAGraph:
    """Manages the entire graph, including all nodes and their connections."""
    def __init__(self):
        """Constructor for the DSAGraph."""
        # The master list of all DSAGraphNode objects in the graph.
        self._vertices = DSALinkedList()

    def add_vertex(self, label):
        """Adds a new vertex to the graph if it doesn't already exist."""
        if self.get_vertex(label) is None:
            self._vertices.insertLast(DSAGraphNode(label))

    def add_edge(self, label1, label2):
        """Adds an undirected edge between two vertices."""
        vertex1 = self.get_vertex(label1)
        vertex2 = self.get_vertex(label2)
        # Ensure both vertices exist before adding a connection.
        if vertex1 and vertex2:
            vertex1.add_edge(vertex2)  # Add edge from V1 to V2.
            vertex2.add_edge(vertex1)  # Add edge from V2 to V1.

    def delete_edge(self, label1, label2):
        """Deletes an undirected edge between two vertices."""
        vertex1 = self.get_vertex(label1) # Find the actual node object corresponding to the first label.
        vertex2 = self.get_vertex(label2) # Find the actual node object corresponding to the second label.
        if vertex1 and vertex2:
            try:
                # Remove the connection from both nodes' adjacency lists.
                vertex1.remove_edge(vertex2)
                vertex2.remove_edge(vertex1)
                print(f"Edge between '{label1}' and '{label2}' deleted.")
            except ValueError:
                print(f"Error: Edge between '{label1}' and '{label2}' does not exist.")
        else:
            print("Error: One or both nodes not found.")

    def delete_node(self, label):
        """Deletes a vertex and all edges connected to it."""
        node_to_delete = self.get_vertex(label) # Find the actual node object that corresponds to the given label.
        if node_to_delete:
            # First, iterate through all neighbors and remove edges pointing to this node.
            sorted_neighbors = node_to_delete.get_adjacent_sorted()  # Get a sorted list of all neighbors connected to the node we're deleting.
            for neighbor in sorted_neighbors: # Loop through each neighbor of the node we are deleting.
                neighbor.remove_edge(node_to_delete)  # Tell each neighbor to remove its connection to the node we're deleting.
            
            # Finally, remove the node itself from the graph's master list.
            self._vertices.remove(node_to_delete)
            print(f"Node '{label}' and its edges have been deleted.")
        else:
            print(f"Error: Node '{label}' not found.")

    def get_vertex(self, label):
        """Finds and returns a vertex node object by its label."""
        current_node = self._vertices.head # Start the search from the beginning (head) of the graph's master vertex list.
        while current_node is not None:
            if current_node.value.get_label() == label: # Check if the current node's label matches the label we are looking for.
                return current_node.value # If it matches, return the actual node object and exit the method.
            current_node = current_node.next   # If it doesn't match, move to the next node in the list.
        return None # If the loop finishes without finding a match, return None.

    def display_as_list(self):
        """Prints the graph structure as an adjacency list."""
        print("\n--- Adjacency List ---")
        vertex_node = self._vertices.head  # Start the iteration at the beginning (head) of the graph's master vertex list.
        if vertex_node is None: print("Graph is empty."); return
        while vertex_node is not None:
            vertex = vertex_node.value # Get the actual DSAGraphNode object from the current list node.
            print(f"{vertex.get_label()}: ", end="") # Print the label of the current vertex (e.g., "A: ").
            adj_node = vertex.get_adjacent().head # Start an inner loop at the beginning of this vertex's own adjacency list.
            while adj_node is not None:  # Loop as long as there are neighbors in the adjacency list.
                print(f" -> {adj_node.value.get_label()}", end="") # Print the label of the current neighbor.
                adj_node = adj_node.next  # Move to the next neighbor in the list.
            print() # Newline for the next vertex.
            vertex_node = vertex_node.next # Move the outer loop to the next vertex in the main graph list.
        print("----------------------")

    def display_as_matrix(self):
        """Builds and prints the graph structure as an adjacency matrix."""
        print("\n--- Adjacency Matrix ---")
        labels = []
        current_node = self._vertices.head # Start at the beginning of the graph's master vertex list.
        while current_node is not None: # Loop through all vertices in the graph.
            labels.append(current_node.value.get_label()) # Add the label of the current vertex to our temporary list.
            current_node = current_node.next  # Move to the next vertex.
        
        # Manually sort labels using an adapted bubble sort.
        n = len(labels)
        for i in range(n): # Start the outer loop of the bubble sort.
            for j in range(0, n - i - 1):  # Start the inner loop for comparing adjacent elements.
                if labels[j] > labels[j+1]: # If the current label is greater than the next one...
                    labels[j], labels[j+1] = labels[j+1], labels[j]  # ...swap their positions in the list.

        # Create a mapping from label to matrix index (e.g., 'A' -> 0).
        index_map = {labels[i]: i for i in range(len(labels))}  # Create a dictionary to map each label to its index (e.g., 'A' -> 0, 'B' -> 1).
        num_vertices = len(labels) # Store the total number of vertices for convenience.
        
        # Manually create a 2D list (matrix) and initialize with zeros.
        matrix = []
        for i in range(num_vertices):
            row = [0] * num_vertices
            matrix.append(row)

        # Iterate through the graph to populate the matrix with ones.
        current_vertex_node = self._vertices.head
        while current_vertex_node is not None: # Loop through each vertex in the graph.
            vertex = current_vertex_node.value # Get the actual vertex object.
            row_index = index_map[vertex.get_label()] # Use the index_map to find the correct row for this vertex.
            current_adjacent_node = vertex.get_adjacent().head  # Start at the beginning of this vertex's own adjacency list.
            while current_adjacent_node is not None:   # Loop through all neighbors of the current vertex.
                adjacent_vertex = current_adjacent_node.value # Get the actual neighbor object.
                col_index = index_map[adjacent_vertex.get_label()]   # Use the index_map to find the correct column for this neighbor.
                matrix[row_index][col_index] = 1  # Place a '1' in the matrix to represent the connection.
                current_adjacent_node = current_adjacent_node.next  # Move to the next neighbor.
            current_vertex_node = current_vertex_node.next  # Move to the next vertex in the main graph list.

        # Print the formatted matrix.
        print("   " + "  ".join(labels)) # Print column headers.
        for i in range(num_vertices):
            print(f"{labels[i]}  ", end="") # Print row header.
            for j in range(num_vertices):
                print(f"{matrix[i][j]}  ", end="") # Print matrix values.
            print()
        print("------------------------")

    def _clear_all_visited(self):
        """Helper method to reset all visited flags before a traversal."""
        current_node = self._vertices.head
        while current_node is not None:
            current_node.value.clear_visited()
            current_node = current_node.next
            
    def _format_traversal_output(self, linked_list):
        """Helper to convert a DSALinkedList of labels into a printable string."""
        output = [] # Create an empty, temporary Python list to hold the values.
        current_node = linked_list.head # Start at the beginning (head) of the input linked list.
        while current_node is not None:
            output.append(current_node.value)  # Add the value from the current list node to our temporary Python list.
            current_node = current_node.next    # Move to the next node in the list.
        return ", ".join(output)  # Use the join method to create a single string of items separated by ", ".

    def breadth_first_search(self, start_label):
        """Performs a Breadth-First Search (BFS) and prints the result."""
        self._clear_all_visited() # Call a helper method to reset the 'visited' flag on all nodes before starting.
        start_vertex = self.get_vertex(start_label) # Find the actual node object that corresponds to the starting label.
        if start_vertex is None: return  # If the starting node doesn't exist, exit the method.

        queue = DSAQueue() # Create a new, empty queue to manage which nodes to visit next.
        traversal_order = DSALinkedList()   # Create a new, empty linked list to store the final traversal order.

        start_vertex.set_visited() # Mark the starting node as visited so we don't visit it again.
        queue.enqueue(start_vertex) # Add the starting node to the queue to begin the search.

        while not queue.is_empty(): # Loop as long as there are nodes in the queue left to process.
            current_vertex = queue.dequeue()  # Remove the node from the front of the queue to process it.
            traversal_order.insertLast(current_vertex.get_label())  # Add the label of this node to our final result list.
            
            sorted_neighbors = current_vertex.get_adjacent_sorted() # Get a sorted list of all neighbors connected to the current node.
            for adjacent_vertex in sorted_neighbors:  # Loop through each of the neighbors.
                if not adjacent_vertex.get_visited(): # Check if this neighbor has already been visited.
                    adjacent_vertex.set_visited()  # If not, mark it as visited.
                    queue.enqueue(adjacent_vertex)  # Add it to the back of the queue to be processed later.
        
        print(f"BFS Order: {self._format_traversal_output(traversal_order)}")

    def depth_first_search(self, start_label):
        """Performs a Depth-First Search (DFS) and prints the result."""
        self._clear_all_visited()
        start_vertex = self.get_vertex(start_label)
        if start_vertex is None: return

        stack = DSAStack()  # Create a new, empty stack to manage which nodes to visit next.
        traversal_order = DSALinkedList()  # Create a new, empty linked list to store the final traversal order.

        stack.push(start_vertex)  # Add the starting node to the stack to begin the search.
        
        while not stack.is_empty():
            current_vertex = stack.pop() # Remove the node from the top of the stack to process it.
            if not current_vertex.get_visited(): # Check if this node has already been visited.
                current_vertex.set_visited() # If not, mark it as visited.
                traversal_order.insertLast(current_vertex.get_label())   # Add the label of this node to our final result list.

                sorted_neighbors = current_vertex.get_adjacent_sorted()  # Get a sorted list of all neighbors of the current node.
                # Push neighbors in reverse sorted order to process them alphabetically.
                i = len(sorted_neighbors) - 1 # Initialize a counter to the last index of the neighbors list.
                while i >= 0:  # Loop backwards through the neighbors list.
                    adjacent_vertex = sorted_neighbors[i]    # Get the neighbor at the current index.
                    if not adjacent_vertex.get_visited():  # Check if this neighbor has been visited yet.
                        stack.push(adjacent_vertex)  # If not, push it onto the stack.
                    i -= 1 # Decrement the counter to move to the previous neighbor.

        print(f"DFS Order: {self._format_traversal_output(traversal_order)}")

# =================================================================
# Main code to run the Interactive Menu
# =================================================================
if __name__ == "__main__":
    # Create an instance of the graph to be used by the menu.
    my_graph = DSAGraph()
    print("Graph program started. Loading sample graph...")
    
    # Pre-load a sample graph for easy testing.
    vertices = ['A', 'B', 'C', 'D', 'E']
    my_graph.add_vertex('F')
    for v in vertices: my_graph.add_vertex(v)
    my_graph.add_edge('A', 'B'); my_graph.add_edge('A', 'C')
    my_graph.add_edge('B', 'D'); my_graph.add_edge('B', 'E')
    my_graph.add_edge('C', 'E'); my_graph.add_edge('D', 'E')

    # Start the main loop for the interactive menu.
    running = True
    while running:
        print("\n--- Graph Operations Menu ---")
        print("1. Add Node | 2. Add Edge | 3. Delete Node | 4. Delete Edge")
        print("5. Display List | 6. Display Matrix | 7. BFS | 8. DFS")
        print("0. Clear/New Graph | 9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            label = input("Enter node label: ").strip().upper()
            my_graph.add_vertex(label); print(f"Node '{label}' added.")
        elif choice == '2':
            l1 = input("Enter first node: ").strip().upper()
            l2 = input("Enter second node: ").strip().upper()
            my_graph.add_edge(l1, l2)
        elif choice == '3':
            label = input("Enter node to delete: ").strip().upper()
            my_graph.delete_node(label)
        elif choice == '4':
            l1 = input("Enter first node of edge: ").strip().upper()
            l2 = input("Enter second node of edge: ").strip().upper()
            my_graph.delete_edge(l1, l2)
        elif choice == '5':
            my_graph.display_as_list()
        elif choice == '6':
            my_graph.display_as_matrix()
        elif choice == '7':
            label = input("Enter start node for BFS: ").strip().upper()
            my_graph.breadth_first_search(label)
        elif choice == '8':
            label = input("Enter start node for DFS: ").strip().upper()
            my_graph.depth_first_search(label)
        elif choice == '0':
            my_graph = DSAGraph()
            print("Graph has been cleared. A new empty graph is ready.")
        elif choice == '9':
            running = False
        else:
            print("Invalid choice.")