import math # for the square root calculation in the prime number finder.
import numpy as np 

class DSAHashEntry:
    """
    A companion class for DSAHashTable to store each entry.
    """
    def __init__(self, key=None, value=None):
        self.key = key # Stores the key for this entry (e.g., a student ID).
        self.value = value # Stores the value associated with the key (e.g., a student name).
        self.state = 0  # Initializes the state of this entry to 0, 0:FREE(never used), 1:USED, -1:PREVIOUSLY_USED(now empty)


class DSAHashTable:
    """
    A class to implement a fully-featured, resizable hash table with 
    DOUBLE HASHING and File I/O capabilities.
    """
    UPPER_THRESHOLD = 0.7 # A class constant defining the load factor at which the table should grow.
    LOWER_THRESHOLD = 0.3 # A class constant defining the load factor at which the table should shrink.
    INITIAL_CAPACITY = 11 # A class constant for the default starting size of the table.

    def __init__(self, table_size=INITIAL_CAPACITY): # The constructor for creating a new hash table.
        actual_size = self._find_next_prime(table_size) # Calculates the actual size by finding the next prime number.
        self.hash_array = np.empty(actual_size, dtype=object) # Creates the internal array, filling it with empty DSAHashEntry objects.
        for i in range(actual_size):
            self.hash_array[i] = DSAHashEntry()  

        self.count = 0 # Initializes the count of items in the table to zero.
    
    # Method to add or update a key-value pair.
    def put(self, key, value):
        if self.get_load_factor() >= self.UPPER_THRESHOLD: # Checks if the table is too full before adding.
            self._resize(len(self.hash_array) * 2) # If too full, calls the resize method to double its capacity.
        
        hash_idx = self._hash(key) # Calculates the initial hash index for the given key.
        orig_idx = hash_idx # Stores the original index to detect if we've looped through the whole table.
        
        if self.hash_array[hash_idx].state == 1: # Checks if the initial slot is already USED (a collision).
            step_size = self._step_hash(key) # If it's a collision, calculates a step size for probing.
            while self.hash_array[hash_idx].state == 1:  # Loops until an empty or previously-used slot is found.
                if self.hash_array[hash_idx].key == key: # Checks if the current slot contains the same key.
                    self.hash_array[hash_idx].value = value # If so, updates the value and exits.
                    return # Exits the method after updating.
                
                hash_idx = (hash_idx + step_size) % len(self.hash_array) # Moves to the next slot using the step size (probing).
                
                if hash_idx == orig_idx: # Checks if we've returned to the starting index.
                    raise Exception("Hash table is full.") # If so, the table is full and no more items can be added.

        self.hash_array[hash_idx].key = key # Once an empty slot is found, sets the key.
        self.hash_array[hash_idx].value = value # Sets the value.
        self.hash_array[hash_idx].state = 1 # Marks the state as 1 (USED).
        self.count += 1 # Increments the total count of items in the table.

    # Method to retrieve the value for a given key.
    def get(self, key):
        found, hash_idx = self._find(key) # Calls the private _find method to locate the key.
        if not found: # Checks if the key was not found.
            raise KeyError(f"Key '{key}' not found.") # If not found, raises an error.
        return self.hash_array[hash_idx].value # If found, returns the value from that entry.

    # Method to check if a key exists in the table.
    def has_key(self, key): 
        found, _ = self._find(key)  # Calls the private _find method.
        return found # Returns True if found, False otherwise.
        
    # Method to remove a key-value pair from the table.
    def remove(self, key): 
        found, hash_idx = self._find(key) # Calls the private _find method to locate the key.
        if not found:
            raise KeyError(f"Key '{key}' not found.")

        removed_value = self.hash_array[hash_idx].value  # Stores the value of the item to be removed.
        self.hash_array[hash_idx].state = -1 # Marks the state as -1 (PREVIOUSLY_USED) instead of deleting.
        self.count -= 1 # Decrements the total count of items.


        if len(self.hash_array) > self.INITIAL_CAPACITY and self.get_load_factor() < self.LOWER_THRESHOLD: # Checks if the table is too empty after removal.
            self._resize(len(self.hash_array) // 2) # If too empty, calls the resize method to halve its capacity.


        return removed_value
    
    # Method to read data from a CSV file and populate the table.
    def read_csv(self, filename): 
        print(f"Reading data from '{filename}'...") 
        try: # Starts a try block to handle potential file errors.
            with open(filename, 'r') as file: # Opens the specified file for reading.
                for line in file: # Loops through each line in the file.
                    parts = line.strip().split(',') # Removes whitespace and splits the line by the comma.
                    if len(parts) == 2: # Checks if the line contains exactly two parts (key and value).
                        key, value = parts[0], parts[1] # Assigns the parts to key and value.
                        self.put(key, value) # Adds the key-value pair to the hash table.
            print("Finished reading data.")
        except FileNotFoundError: # Catches the error if the file doesn't exist.
            print(f"Error: Could not find the file '{filename}'.")

    # Method to save the table's contents to a CSV file.
    def save_csv(self, filename):
        print(f"Saving hash table to '{filename}'...")
        with open(filename, 'w') as file: # Opens the specified file for writing (will overwrite existing file).
            for entry in self.hash_array: # Loops through every entry in the internal array.
                if entry.state == 1: # Checks if the entry is currently USED.
                    file.write(f"{entry.key},{entry.value}\n") # If so, writes the key and value to the file in CSV format.
        print("Save complete.")

    # A private method to handle resizing the table.
    def _resize(self, new_size_suggestion):
        print(f"--- RESIZING: Load factor is {self.get_load_factor():.2f}. Old size: {len(self.hash_array)} ---") # Prints a status message.
        old_array = self.hash_array # Temporarily stores the old array.
        new_actual_size = self._find_next_prime(new_size_suggestion) # Calculates the new prime size for the new array.
        
        self.hash_array = np.empty(new_actual_size, dtype=object)
        for i in range(new_actual_size):
            self.hash_array[i] = DSAHashEntry() # Creates a new, empty array of the new size.
        
        self.count = 0 # Resets the item count to zero.
        for entry in old_array: # Loops through every entry in the old array.
            if entry.state == 1: # Checks if the old entry was USED.
                self.put(entry.key, entry.value) # If so, re-hashes and inserts it into the new array.
        print(f"--- RESIZE COMPLETE: New size is {len(self.hash_array)} ---")  # Prints a completion message.
        
    # A private helper method to locate a key in the table.    
    def _find(self, key):
        hash_idx = self._hash(key) # Calculates the initial hash index.
        orig_idx = hash_idx  # Stores the original index to detect a full loop.
        step_size = self._step_hash(key) # Calculates the step size for probing.
        while self.hash_array[hash_idx].state != 0: # Loops until a FREE (never-used) slot is found.
            if self.hash_array[hash_idx].state == 1 and self.hash_array[hash_idx].key == key: # Checks if the current slot is USED and contains the correct key.
                return (True, hash_idx)  # If so, returns True and the index.
            hash_idx = (hash_idx + step_size) % len(self.hash_array) # Moves to the next slot using the step size.
            if hash_idx == orig_idx: return (False, -1) # If we've looped back to the start, the key is not here.
        return (False, -1) # If we hit a FREE slot, the key is not in the table.

     # The primary hash function.
    def _hash(self, key):
        hash_idx = 0 # Initializes the hash index to zero.
        for char in key: # Loops through each character in the key string.
            hash_idx = (33 * hash_idx) + ord(char) # Applies a formula (Bernstein hash variant) to update the index.
        return hash_idx % len(self.hash_array) # Returns the final index, wrapped to fit the array size.

    # The secondary hash function for calculating the probe step size.
    def _step_hash(self, key):
        MAX_STEP = 5 # Defines a maximum step size (a small prime number).
        int_val = 0 # Initializes an integer value to zero.
        for char in key:  # Loops through each character in the key.
            int_val += ord(char)  # Adds the character's code to the integer value.
        return MAX_STEP - (int_val % MAX_STEP) # Returns a step size between 1 and MAX_STEP.

    # A helper method to find the next prime number.
    def _find_next_prime(self, start_val): 
        if start_val < 2: return 2 # Handles cases where the start value is less than 2.
        prime_val = start_val | 1 # A bitwise trick to make the number odd.
        if prime_val < start_val: prime_val +=2  # Ensures the candidate is greater than or equal to start_val.
        is_prime = False # A flag to control the loop.
        while not is_prime: # Loops until a prime number is found.
            is_prime = True # Assumes the current number is prime.
            root_val = int(math.sqrt(prime_val))  # Calculates the square root to optimize the check.
            
            i = 3 # Start checking divisors from 3.
            still_checking = True # A flag to control this inner loop.
            while i <= root_val and still_checking: # Loop while there are still divisors to check.
                if prime_val % i == 0: # Checks for divisibility.
                    is_prime = False # If divisible, it's not prime.
                    still_checking = False # Set flag to false to stop this inner loop.
                i += 2 # Move to the next odd divisor.
            
            if not is_prime: # If the number was found to not be prime.
                prime_val += 2 # Moves to the next odd number to test.
        return prime_val # Returns the found prime number.
    
    # Method to calculate the current load factor.
    def get_load_factor(self):
        return self.count / len(self.hash_array)  # Divides the number of items by the total capacity.

    def display(self):
        print(f"\n----- HASH TABLE (Size: {len(self.hash_array)}, Count: {self.count}) -----")
        for i, entry in enumerate(self.hash_array): # Loops through the internal array with indices.
            if entry.state == 1: # Checks if the entry is USED.
                print(f"Index {i}: Key='{entry.key}', Value={entry.value}")  # Prints the details of the entry.
        print("-----------------------------------------------------------\n")

#=====================================================================#
#                         INTERACTIVE MENU                            #
#=====================================================================#

def print_menu():
    """Prints the menu of options."""
    print("\n--- Hash Table Menu ---")
    print("1. Add item")
    print("2. Get item value")
    print("3. Remove item")
    print("4. Check if item exists")
    print("5. Display hash table")
    print("6. Show load factor")
    print("7. Read CSV file")
    print("8. Save to CSV file")
    print("0. Exit")
    print("-----------------------")

def main():
    """Main function to run the interactive menu."""
    my_table = DSAHashTable()

    is_running = True
    while is_running:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting program. Goodbye!")
            is_running = False
        
        elif choice == '1':
            key = input("Enter key: ")
            value = input("Enter value: ")
            my_table.put(key, value)
            print(f"Added/updated '{key}'.")
        
        elif choice == '2':
            key = input("Enter key to get value for: ")
            try:
                value = my_table.get(key)
                print(f"Value for '{key}' is: {value}")
            except KeyError as e:
                print(e)
        
        elif choice == '3':
            key = input("Enter key to remove: ")
            try:
                removed_value = my_table.remove(key)
                print(f"Removed '{key}'. Its value was: {removed_value}")
            except KeyError as e:
                print(e)

        elif choice == '4':
            key = input("Enter key to check: ")
            exists = my_table.has_key(key)
            print(f"Does the key '{key}' exist? {exists}")
            
        elif choice == '5':
            my_table.display()
            
        elif choice == '6':
            lf = my_table.get_load_factor()
            print(f"Current Load Factor: {lf:.2f} ({my_table.count}/{len(my_table.hash_array)})")

        elif choice == '7':
            filename = input("Enter CSV filename to read (e.g., RandomNames7000.csv): ")
            my_table.read_csv(filename)
            
        elif choice == '8':
            filename = input("Enter filename to save to (e.g., export.csv): ")
            my_table.save_csv(filename)
        
        else:
            print("Invalid choice. Please enter a number from 0 to 8.")

if __name__ == "__main__":
    main()