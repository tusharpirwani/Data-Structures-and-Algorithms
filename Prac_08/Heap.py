import math 
import numpy as np 

class DSAHeapEntry: 
    """
    A companion class to store each entry in the heap.
    It holds an integer priority (key) and a string value.
    """
    def __init__(self, priority, value): # The constructor method, called when a new DSAHeapEntry is created.
        self.priority = priority # Stores the priority (an integer) of the entry.
        self.value = value # Stores the value (a string) associated with the priority.

class DSAHeap: # Defines the main class for the heap data structure.
    """
    A class that implements the heap data structure with an interactive menu.
    """
    def __init__(self, max_size): # The constructor for creating a new heap instance.
        """Initializes the heap with a maximum capacity."""
        self.heap = np.full(max_size, None, dtype=object) # Initialized a NumPy array of objects, filled with None
        self.count = 0 # Initializes a counter for the number of items currently in the heap.

    def add(self, priority, value): # Defines the method for adding a new item to the heap.
        """Adds an entry to the heap and trickles it up to the correct position."""
        if self.count >= len(self.heap): # Checks if the heap's internal list is already full.
            raise Exception("Heap is full.") # If full, raises an error to prevent overflow.
        
        self.heap[self.count] = DSAHeapEntry(priority, value) # Creates a new DSAHeapEntry object and places it at the next available spot.
        self._trickleUp(self.count) # Calls the _trickleUp helper to move the new item to its correct position.
        self.count += 1 # Increments the counter of items in the heap.

    def remove(self): # Defines the method for removing the highest-priority item.
        """Removes and returns the entry with the highest priority (the root)."""
        if self.count == 0: # Checks if the heap is empty.
            raise Exception("Heap is empty.") # If empty, raises an error as there is nothing to remove.

        removed_entry = self.heap[0] # Stores the root element (the max item) to be returned later.
        last_idx = self.count - 1 # Calculates the index of the last item in the heap.
        self.heap[0] = self.heap[last_idx] # Moves the last item to the root position.
        self.heap[last_idx] = None # Clears the original spot of the last item to prevent duplicate data.
        self.count -= 1 # Decrements the item counter.
        self._trickleDown(0) # Calls the _trickleDown helper to restore the heap property from the new root.
        
        return removed_entry # Returns the highest-priority item that was removed.
    
    def heapify(self): # Defines the method to convert the internal array into a valid max-heap.
        """Builds the heap from an unsorted array stored internally."""
        num_items = self.count # Gets the current number of items.
        for i in range((num_items // 2) - 1, -1, -1): # Loops backwards from the last parent node up to the root.
            self._trickleDown(i) # Calls _trickleDown on each parent to enforce the heap property.

    def heapSort(self): # Defines the method to sort the items in the heap.
        """Sorts the heap's internal array in ascending order."""
        original_count = self.count # Saves the original number of items.
        
        for i in range(original_count - 1, 0, -1): # Loops backwards from the last index down to the second element.
            temp = self.heap[0] # Temporarily stores the root (max element).
            self.heap[0] = self.heap[i] # Swaps the last unsorted element into the root position.
            self.heap[i] = temp # Places the max element at the end of the unsorted portion.
            
            self.count -= 1 # Logically shrinks the heap size by one for the next iteration.
            self._trickleDown(0) # Re-heapifies the reduced heap by trickling down the new root.
            
        self.count = original_count # Restores the original count after the sort is complete.

    def display(self): # Defines a method to print the heap's contents.
        """Prints the current contents of the heap or sorted array."""
        print(f"\n----- Heap/Array (Count: {self.count}, Capacity: {len(self.heap)}) -----") # Prints a header with status info.
        limit = self.count # Sets the default number of items to print to the current count.
        if self.count > 1 and self.heap[0].priority < self.heap[self.count-1].priority: # A simple check to guess if the array is sorted.
            limit = len(self.heap) # If it looks sorted, set the limit to the full capacity to show all items.

        for i in range(limit): # Loops up to the determined limit.
            entry = self.heap[i] # Gets the entry at the current index.
            if entry is not None: # Checks to ensure the entry is not empty.
                print(f"Index {i}: Priority={entry.priority}, Value='{entry.value}'") # Prints the details of the entry.
        print("-----------------------------------------------------------\n") # Prints a footer for clean formatting.

    def _trickleDown(self, index): # Defines the private helper for the trickle-down algorithm.
        """Moves a node down the heap to maintain the heap property."""
        left_idx = 2 * index + 1 # Calculates the index of the left child.
        right_idx = 2 * index + 2 # Calculates the index of the right child.

        while left_idx < self.count: # Continues as long as the current node has at least a left child.
            large_idx = left_idx # Assumes the left child has the higher priority.
            
            if right_idx < self.count: # Checks if a right child exists within the heap.
                if self.heap[left_idx].priority < self.heap[right_idx].priority: # Compares the priorities of the two children.
                    large_idx = right_idx # If the right child is larger, it becomes the one to compare with the parent.
            
            if self.heap[large_idx].priority > self.heap[index].priority: # Checks if the largest child's priority is greater than its parent's.
                temp = self.heap[large_idx] # Temporarily stores the child entry.
                self.heap[large_idx] = self.heap[index] # Moves the parent down to the child's position.
                self.heap[index] = temp # Moves the child up to the parent's position.

                index = large_idx # Updates the current index to the position of the swapped child.
                left_idx = 2 * index + 1 # Recalculates the left child index for the next iteration.
                right_idx = 2 * index + 2 # Recalculates the right child index.
            else: # If the parent is already greater than or equal to its largest child.
                left_idx = self.count # Sets the loop condition to false to terminate the process.

    def _trickleUp(self, index): # Defines the private helper for the trickle-up algorithm.
        """Moves a node up the heap to maintain the heap property."""
        parent_idx = (index - 1) // 2 # Calculates the index of the parent node.
        
        while index > 0 and self.heap[index].priority > self.heap[parent_idx].priority: # Loops while not at the root and the child is larger than its parent.
            temp = self.heap[parent_idx] # Temporarily stores the parent entry.
            self.heap[parent_idx] = self.heap[index] # Moves the child up to the parent's position.
            self.heap[index] = temp # Moves the parent down to the child's original position.
            
            index = parent_idx # Updates the current index to the parent's position to continue moving up.
            parent_idx = (index - 1) // 2 # Recalculates the new parent's index.

#=====================================================================#
#                         INTERACTIVE MENU                            #
#=====================================================================#

def print_menu(): 
    """Prints the menu of options."""
    print("\n--- Heap Menu ---") 
    print("1. Add item") 
    print("2. Remove max item") 
    print("3. Sort the array (Heap Sort)") 
    print("4. Display heap/array") 
    print("5. Load from CSV and Heapify") 
    print("6. Save sorted array to CSV")
    print("0. Exit") 
    print("-----------------") 

def main():
    """Main function to run the interactive menu."""
   
    heap_size = 0
    is_valid_size = False
    while not is_valid_size:
        size_input = input("Enter the maximum size for the heap: ")
        try:
            heap_size = int(size_input)
            if heap_size > 0:
                is_valid_size = True
            else:
                print("Error: Please enter a positive number.")
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")
    
    my_heap = DSAHeap(heap_size)

    is_running = True
    while is_running:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting program.")
            is_running = False
        
        elif choice == '1':
            try:
                priority = int(input("Enter priority (integer): "))
                value = input("Enter value (string): ")
                my_heap.add(priority, value)
                print(f"Added entry with priority {priority}.")
            except ValueError:
                print("Error: Priority must be an integer.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            try:
                removed = my_heap.remove()
                print(f"Removed max item: Priority={removed.priority}, Value='{removed.value}'")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            print("Sorting the array using Heap Sort...")
            my_heap.heapSort()
            print("Sort complete. Use 'Display' to see the sorted array.")

        elif choice == '4':
            my_heap.display()
            
        elif choice == '5':
            filename = input("Enter CSV filename to load (e.g., RandomNames7000.csv): ")
            try:
                temp_list = []
                with open(filename, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            temp_list.append(DSAHeapEntry(int(parts[0]), parts[1]))
                
                if len(temp_list) > len(my_heap.heap):
                    print(f"Error: File contains {len(temp_list)} items, but heap capacity is only {len(my_heap.heap)}.")
                else:
                    my_heap.count = 0
                    for i, entry in enumerate(temp_list):
                        my_heap.heap[i] = entry
                    my_heap.count = len(temp_list)
                    
                    print("Data loaded. Now heapifying...")
                    my_heap.heapify()
                    print("Heap built successfully.")

            except FileNotFoundError:
                print(f"Error: Could not find the file '{filename}'.")
            except ValueError:
                print("Error: CSV file contains non-integer priorities.")
            
        elif choice == '6':
            filename = input("Enter filename to save to (e.g., sorted_names.csv): ")
            try:
                with open(filename, 'w') as file:
                    for entry in my_heap.heap:
                        if entry is not None:
                            file.write(f"{entry.priority},{entry.value}\n")
                print(f"Sorted data saved to '{filename}'.")
            except IOError:
                print(f"Error: Could not write to the file '{filename}'.")
        
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()