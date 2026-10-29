# =================================================================
# File: module1_graph.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Implements graph data structures (DSAGraphNode, DSAGraph)
#          and algorithms (BFS, DFS, Dijkstra's) for hospital navigation.
#          Graph structure adapted from Practical 6.
# =================================================================

from dsa_linked_list import DSALinkedList
from dsa_stacks_queues import DSAStack, DSAQueue

class DSAGraphNode:
    """
    Represents a single vertex (node/department) in the graph.
    Includes attributes for traversal algorithms (Dijkstra's, DFS cycle check).
    """
    def __init__(self, p_label):
        """Constructor for a DSAGraphNode."""
        self._label = p_label  # The name of the department (e.g., 'Pharmacy')
        self._links = DSALinkedList() # Adjacency list: stores (neighbor_node, weight) tuples
        self._visited = False  # Flag for BFS/DFS traversals
        self._distance = float('inf') # Use float('inf') for Dijkstra's distance initialization
        self._previous = None  # Previous node in the shortest path (for Dijkstra's)
        self._in_path = False  # Flag for detecting cycles in DFS

    # --- Basic Getters / Setters (Module 1) ---
    def get_label(self): 
        """Returns the label of the node."""
        return self._label
    
    def get_adjacent(self): 
        """Returns the linked list of adjacent nodes (neighbors)."""
        return self._links
    
    def add_edge(self, vertex, weight): 
        """Adds a weighted connection (edge) from this node to another."""
        # Ensure weight is a number
        try:
            numeric_weight = float(weight)
            if numeric_weight < 0:
                 print(f"Warning: Edge weight between {self._label} and {vertex.get_label()} is negative ({weight}). Dijkstra's may not work correctly.")
            self._links.insertLast((vertex, numeric_weight)) # Inserts a tuple (node_object, weight)
        except ValueError:
             print(f"Error: Edge weight '{weight}' between {self._label} and {vertex.get_label()} is not a valid number. Edge not added.")

        
    def remove_edge(self, vertex_to_remove): 
        """Removes a connection from this node to another."""
        current = self._links.head
        found = False
        while current is not None and not found:
            neighbor_node, weight = current.value
            if neighbor_node == vertex_to_remove:
                self._links.remove(current.value) # Remove the tuple
                found = True
            else:
                current = current.next
        if not found:
            # This case should ideally not happen if add_edge ensures symmetry, but good to handle
            print(f"Warning: Tried to remove edge to {vertex_to_remove.get_label()} from {self._label}, but it wasn't found.")

    
    def set_visited(self): 
        """Marks the node as visited."""
        self._visited = True
        
    def clear_visited(self): 
        """Resets the visited flag to False."""
        self._visited = False
        
    def get_visited(self): 
        """Checks if the node has been visited."""
        return self._visited
    
    def set_distance(self, dist): 
        """Sets the calculated distance (for Dijkstra's)."""
        self._distance = dist
        
    def get_distance(self): 
        """Gets the calculated distance (for Dijkstra's)."""
        return self._distance
        
    def set_previous(self, node): 
        """Sets the previous node in a path (for Dijkstra's)."""
        self._previous = node
        
    def get_previous(self): 
        """Gets the previous node in a path (for Dijkstra's)."""
        return self._previous
        
    def set_in_path(self, in_path_status): 
        """Sets the flag for DFS cycle detection (True if node is in current recursion stack)."""
        self._in_path = in_path_status
        
    def get_in_path(self): 
        """Gets the flag for DFS cycle detection."""
        return self._in_path

    # --- Sorting and String methods ---
    def _sort_neighbors(self, temp_list):
        """
        Sorts neighbor tuples using a manual bubble sort.
        This ensures a consistent (alphabetical) traversal order for BFS/DFS.
        Sorts based on the neighbor's label (the first element of the tuple, index [0]).
        """
        n = 0
        for _ in temp_list: n += 1 # Manually get length of list
        
        i = 0
        while i < n: # Outer loop of bubble sort
            j = 0
            while j < (n - i - 1): # Inner loop for comparisons
                # Compare labels (e.g., 'Pharmacy' > 'ICU')
                if temp_list[j][0].get_label() > temp_list[j+1][0].get_label():
                    # Perform the swap
                    temp_list[j], temp_list[j+1] = temp_list[j+1], temp_list[j]
                j += 1
            i += 1
        return temp_list

    def get_adjacent_sorted(self):
        """
        Returns a sorted Python list of adjacent (node, weight) tuples.
        This is a helper for traversal algorithms to ensure alphabetical processing.
        """
        adj_list = [] # A temporary Python list
        current_node = self._links.head # Start at the head of the adjacency list
        while current_node is not None:
            adj_list.append(current_node.value) # Add the (node, weight) tuple
            current_node = current_node.next
        return self._sort_neighbors(adj_list) # Return the sorted list

    def __str__(self):
        """Returns the string representation of the node (its label)."""
        return str(self._label)

class DSAGraph:
    """
    Manages the entire graph, including all nodes (departments) and
    their connections (corridors).
    """
    LARGE_NUMBER = float('inf') # Use float('inf') instead of arbitrary large number
    
    def __init__(self):
        """Constructor for the DSAGraph."""
        # _vertices is a Linked List of DSAGraphNode objects
        self._vertices = DSALinkedList()

    # --- Vertex and Edge Management ---
    def add_vertex(self, label):
        """Adds a new vertex (department) to the graph if it doesn't already exist."""
        if self.get_vertex(label) is None:
            new_vertex = DSAGraphNode(label)
            self._vertices.insertLast(new_vertex)
            print(f"Vertex '{label}' added.")
        else:
            print(f"Vertex '{label}' already exists.")


    def add_edge(self, label1, label2, weight):
        """
        Adds an undirected edge between two vertices with a given weight.
        This means adding the edge in both directions (V1 -> V2 and V2 -> V1).
        """
        vertex1 = self.get_vertex(label1)
        vertex2 = self.get_vertex(label2)
        if vertex1 and vertex2:
            # Add edge from V1 to V2
            vertex1.add_edge(vertex2, weight)
            # Add edge from V2 to V1 (ensures symmetry)
            vertex2.add_edge(vertex1, weight)
            print(f"Edge added between '{label1}' and '{label2}' with weight {weight}.")
        else:
            if not vertex1: print(f"Error: Could not add edge. Vertex '{label1}' not found.")
            if not vertex2: print(f"Error: Could not add edge. Vertex '{label2}' not found.")


    def get_vertex(self, label):
        """Finds and returns a vertex node object by its label, or None if not found."""
        current_node = self._vertices.head # Start at the head of the master vertex list
        found_node = None
        # Loop while we haven't reached the end and we haven't found the node
        while current_node is not None and found_node is None:
            if current_node.value.get_label() == label:
                found_node = current_node.value # We found it
            current_node = current_node.next # Move to the next node
        return found_node
    
    def get_all_vertices(self):
        """Returns a Python list of all DSAGraphNode objects in the graph."""
        nodes = []
        current_node = self._vertices.head
        while current_node is not None:
            nodes.append(current_node.value)
            current_node = current_node.next
        return nodes

    # --- Display Methods ---
    def display_as_list(self):
        """Prints the graph structure as a weighted adjacency list."""
        print("\n--- Adjacency List (Weighted) ---")
        vertex_node = self._vertices.head # Start with the first vertex in the graph
        if vertex_node is None: 
            print("Graph is empty.")
        else:
            while vertex_node is not None:
                vertex = vertex_node.value # Get the DSAGraphNode object
                print(f"{vertex.get_label()}: ", end="")
                
                # Iterate through this vertex's own adjacency list
                adj_node = vertex.get_adjacent().head
                is_first = True
                while adj_node is not None:
                    neighbor_node = adj_node.value[0] # The neighbor node object
                    neighbor_weight = adj_node.value[1] # The edge weight
                    if not is_first:
                         print(", ", end="")
                    print(f"{neighbor_node.get_label()} ({neighbor_weight})", end="")
                    is_first = False
                    adj_node = adj_node.next
                print() # Newline for the next vertex
                vertex_node = vertex_node.next
        print("---------------------------------")

    def display_as_matrix(self):
        """Builds and prints the graph structure as a weighted adjacency matrix."""
        print("\n--- Adjacency Matrix (Weighted) ---")
        
        # 1. Get all labels into a Python list
        labels = []
        current_node = self._vertices.head
        while current_node is not None: 
            labels.append(current_node.value.get_label())
            current_node = current_node.next
        
        # 2. Manually Bubble Sort the labels (to get A, B, C... order)
        n = 0
        for _ in labels: n+=1
        i = 0; 
        while i < n:
            j = 0
            while j < (n - i - 1):
                if labels[j] > labels[j+1]: 
                    labels[j], labels[j+1] = labels[j+1], labels[j]
                j += 1
            i += 1

        # 3. Build a "map" to link labels to matrix indices (e.g., 'ICU' -> 0, 'Labs' -> 1)
        # Using a simple list scan approach instead of a dictionary for compliance
        num_vertices = n 
        
        # 4. Initialize an empty matrix (list of lists) with zeros
        matrix = []
        r = 0
        while r < num_vertices: 
            # Initialize with 0, representing no direct connection
            row = [0] * num_vertices 
            matrix.append(row)
            r += 1

        # 5. Populate the matrix with weights
        current_vertex_node = self._vertices.head
        while current_vertex_node is not None:
            vertex = current_vertex_node.value
            
            # Find the row index for this vertex using list scan
            row_index = -1
            k = 0
            while k < n and row_index == -1:
                if labels[k] == vertex.get_label(): 
                    row_index = k
                k += 1
            
            # Go through its neighbors
            current_adjacent_node = vertex.get_adjacent().head
            while current_adjacent_node is not None:
                adjacent_vertex = current_adjacent_node.value[0]
                weight = current_adjacent_node.value[1]
                
                # Find the column index for this neighbor using list scan
                col_index = -1
                k = 0
                while k < n and col_index == -1:
                    if labels[k] == adjacent_vertex.get_label(): 
                        col_index = k
                    k += 1
                    
                if row_index != -1 and col_index != -1:
                    matrix[row_index][col_index] = weight # Set the weight
                    
                current_adjacent_node = current_adjacent_node.next
            current_vertex_node = current_vertex_node.next
        
        # 6. Print the formatted matrix
        # Calculate max label length for formatting
        max_label_len = 0
        k = 0
        while k < n:
             if len(labels[k]) > max_label_len:
                  max_label_len = len(labels[k])
             k += 1
        
        header_padding = max_label_len + 2 # Padding for row labels

        # Print column headers
        print(" " * header_padding + " ".join([f"{lbl:<{max_label_len}}" for lbl in labels])) 
        
        i_idx = 0
        while i_idx < num_vertices:
            # Print row header
            print(f"{labels[i_idx]:<{header_padding}}", end="") 
            j_idx = 0
            while j_idx < n: 
                # Print cell value (0 if no edge, weight otherwise)
                print(f"{matrix[i_idx][j_idx]:<{max_label_len}}", end=" ") 
                j_idx += 1
            print()
            i_idx += 1
        print("---------------------------------")

    # --- Module 1 Algorithms ---
    def _clear_all_visited(self):
        """Helper method to reset all node flags before a new traversal."""
        current_node = self._vertices.head
        while current_node is not None:
            current_node.value.clear_visited()
            current_node.value.set_in_path(False)
            # Reset Dijkstra's data as well
            current_node.value.set_distance(self.LARGE_NUMBER)
            current_node.value.set_previous(None)
            current_node = current_node.next
            
    def _format_traversal_output(self, node_list):
        """Helper to convert a list/linked list of nodes/labels into a printable string."""
        output = [] # Use a temporary Python list
        
        # Check if input is a DSALinkedList or a standard Python list
        if isinstance(node_list, DSALinkedList):
            current_node = node_list.head
            while current_node is not None: 
                # Check if value is a node or just a label
                if isinstance(current_node.value, DSAGraphNode):
                     output.append(current_node.value.get_label())
                else:
                     output.append(str(current_node.value)) # Assume it's a label
                current_node = current_node.next
        else: # Assume it's a standard Python list
             i = 0
             while i < len(node_list):
                  item = node_list[i]
                  if isinstance(item, DSAGraphNode):
                       output.append(item.get_label())
                  else:
                       output.append(str(item))
                  i += 1

        return " -> ".join(output) # Use join for clean formatting

    def breadth_first_search_by_level(self, start_label):
        """
        Performs a Breadth-First Search (BFS) starting from `start_label`.
        Prints the reachable departments, grouped by their level (hops) from the start.
        """
        print(f"\n--- BFS by Level (Start: {start_label}) ---")
        self._clear_all_visited() # Reset all node flags
        start_vertex = self.get_vertex(start_label)
        
        if start_vertex is None: 
            print(f"Error: Start node '{start_label}' not found.")
        else:
            queue = DSAQueue() # Use the custom queue
            start_vertex.set_visited()
            queue.enqueue((start_vertex, 0)) # Enqueue a tuple: (node, level)
            
            output_levels = {} # Use a dictionary-like structure (parallel lists) to store levels
            level_keys = []
            level_values = []
            
            max_level = 0

            while not queue.is_empty():
                current_vertex, current_level = queue.dequeue()
                
                # Store node in the correct level list
                level_str = str(current_level)
                found_level = False
                k = 0
                while k < len(level_keys):
                     if level_keys[k] == level_str:
                          level_values[k].append(current_vertex.get_label())
                          found_level = True
                     k += 1
                
                if not found_level:
                     level_keys.append(level_str)
                     level_values.append([current_vertex.get_label()])

                if current_level > max_level:
                    max_level = current_level
                
                # Get all neighbors, sorted alphabetically
                sorted_neighbors_tuples = current_vertex.get_adjacent_sorted()
                
                i = 0
                while i < len(sorted_neighbors_tuples):
                    adjacent_vertex = sorted_neighbors_tuples[i][0] # Get node from tuple
                    if not adjacent_vertex.get_visited():
                        adjacent_vertex.set_visited() # Mark as visited
                        queue.enqueue((adjacent_vertex, current_level + 1)) # Enqueue with incremented level
                    i += 1

            # Print the collected levels
            level_num = 0
            while level_num <= max_level:
                 level_str_key = str(level_num)
                 nodes_at_level = []
                 k = 0
                 while k < len(level_keys):
                      if level_keys[k] == level_str_key:
                           nodes_at_level = level_values[k]
                      k += 1
                 
                 if len(nodes_at_level) > 0:
                      print(f"Level {level_num}: {', '.join(nodes_at_level)}")
                 level_num += 1

            print("--------------------------------------")

    def depth_first_search_cycle_detect(self, start_label):
        """
        Performs a Depth-First Search (DFS) from a start node to detect cycles.
        Calls a recursive helper function to perform the traversal.
        """
        print(f"\n--- DFS Cycle Detection (Start: {start_label}) ---")
        self._clear_all_visited()
        start_vertex = self.get_vertex(start_label)
        
        if start_vertex is None: 
            print(f"Error: Start node '{start_label}' not found.")
        else:
            path_stack = DSAStack() # Use stack to keep track of the path for reporting cycles
            cycle_found_globally = self._dfs_cycle_helper(start_vertex, path_stack) # Call the recursive helper
            if not cycle_found_globally: 
                print("No cycles found reachable from this node.")
        print("-------------------------------------------")

    def _dfs_cycle_helper(self, current_vertex, path_stack):
        """Recursive helper for DFS. Returns True if a cycle is found."""
        current_vertex.set_visited() # Mark as visited (gray)
        current_vertex.set_in_path(True) # Mark as in the current recursion path
        path_stack.push(current_vertex) # Add to the current path trace

        cycle_found = False
        sorted_neighbors = current_vertex.get_adjacent_sorted()
        
        i = 0
        # Loop while iterating neighbors and a cycle hasn't been found
        while i < len(sorted_neighbors) and not cycle_found:
            (neighbor_node, weight) = sorted_neighbors[i] # Get neighbor node
            
            if not neighbor_node.get_visited():
                # If neighbor is unvisited (white), recurse
                cycle_found = self._dfs_cycle_helper(neighbor_node, path_stack)
            elif neighbor_node.get_in_path():
                # If neighbor is *already in the current path* (gray), we found a back edge
                print(f"Cycle Detected! Path leads back to {neighbor_node.get_label()}.")
                # Construct cycle path string (optional but informative)
                # This requires iterating the stack, which is complex without direct list access
                # For simplicity, just reporting the edge causing the cycle.
                print(f"  (Back edge from {current_vertex.get_label()} to {neighbor_node.get_label()})")
                cycle_found = True
            
            i += 1
            
        current_vertex.set_in_path(False) # Remove from recursion path (black)
        
        # Only pop if the stack is not empty (safety check)
        if not path_stack.is_empty():
            path_stack.pop() # Remove from path trace as we backtrack
        
        return cycle_found

    # Dijkstra's algorithm implementation approach referenced from:
    # Wikipedia contributors. (2025). Dijkstra's algorithm. In Wikipedia, The Free Encyclopedia.
    # from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    def find_shortest_path(self, start_label, end_label):
        """Finds and prints the shortest path using Dijkstra's algorithm."""
        print(f"\n--- Shortest Path (Dijkstra's) ---")
        print(f"From: {start_label} To: {end_label}")
        
        self._clear_all_visited() # Set all distances to infinity, clear visited/previous
        start_vertex = self.get_vertex(start_label)
        end_vertex = self.get_vertex(end_label)
        
        if not start_vertex or not end_vertex: 
            if not start_vertex: print(f"Error: Start department '{start_label}' not found.")
            if not end_vertex: print(f"Error: End department '{end_label}' not found.")
        elif start_label == end_label:
             print("Total time: 0 minutes")
             print(f"Path: {start_label}")
        else:
            start_vertex.set_distance(0) # Distance from start to start is 0
            
            # Priority queue substitute: Use a standard Python list to store nodes to visit
            # This is less efficient than a real priority queue but avoids restricted structures
            unvisited_nodes = self.get_all_vertices()
            
            nodes_remaining = True
            while nodes_remaining:
                
                # Find the unvisited node with the minimum distance
                min_distance = self.LARGE_NUMBER
                current_vertex = None
                
                idx_to_remove = -1 # Keep track of index if using Python list
                i = 0
                while i < len(unvisited_nodes):
                    node = unvisited_nodes[i]
                    if node.get_distance() < min_distance:
                        min_distance = node.get_distance()
                        current_vertex = node
                        idx_to_remove = i
                    i += 1

                # If no reachable unvisited node is found, or we found the destination
                if current_vertex is None or current_vertex == end_vertex or min_distance == self.LARGE_NUMBER:
                    nodes_remaining = False # Stop the loop
                else:
                    # "Visit" the current node by removing it from the list
                    # Manual removal from Python list (avoiding pop/remove)
                    new_unvisited = []
                    j = 0
                    while j < len(unvisited_nodes):
                         if j != idx_to_remove:
                              new_unvisited.append(unvisited_nodes[j])
                         j += 1
                    unvisited_nodes = new_unvisited

                    # Relax all neighbors
                    for (neighbor_node, weight) in current_vertex.get_adjacent_sorted():
                        
                        # Calculate distance through the current node
                        new_distance = current_vertex.get_distance() + weight
                        
                        # If this new path is shorter, update the neighbor's distance and previous node
                        if new_distance < neighbor_node.get_distance():
                            neighbor_node.set_distance(new_distance)
                            neighbor_node.set_previous(current_vertex)
                                
            # --- Path Reconstruction ---
            total_distance = end_vertex.get_distance()
            if total_distance == self.LARGE_NUMBER: 
                print(f"No path found from {start_label} to {end_label}.")
            else:
                # Use a standard Python list to reconstruct path temporarily
                path_nodes_reversed = [] 
                current_on_path = end_vertex
                
                # Work backwards from the end node
                while current_on_path is not None:
                    path_nodes_reversed.append(current_on_path) # Add node object
                    current_on_path = current_on_path.get_previous() # Go to previous node
                
                # Reverse the list manually for correct order
                path_nodes_ordered = []
                idx = len(path_nodes_reversed) - 1
                while idx >= 0:
                     path_nodes_ordered.append(path_nodes_reversed[idx])
                     idx -= 1

                print(f"Total time: {total_distance} minutes")
                print(f"Path: {self._format_traversal_output(path_nodes_ordered)}")
        print("------------------------------------")