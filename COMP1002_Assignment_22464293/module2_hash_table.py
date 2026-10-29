# =================================================================
# File: module2_hash_table.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Implements a Hash Table using Linear Probing for patient lookup.
#          Includes PatientRecord and DSAHashTable classes.
#          Core hashing logic adapted from Practical 7.
# =================================================================

import math
import csv
import numpy as np

class PatientRecord:
    """
    Simple container for patient data.
    This object is stored as the 'value' in the hash table.
    """
    def __init__(self, patient_id, name, urgency, condition, treatment_duration=0):
        """
        Constructor for PatientRecord.
        treatment_duration defaults to 0 and is updated by Module 3.
        """
        self.patient_id = patient_id
        self.name = name
        # Ensure urgency is stored as an integer
        try:
             self.urgency = int(urgency)
        except ValueError:
             print(f"Warning: Invalid urgency '{urgency}' for patient '{patient_id}'. Setting to default 0.")
             self.urgency = 0 # Default or error state

        self.condition = condition
        # Ensure treatment_duration is stored as an integer
        try:
             self.treatment_duration = int(treatment_duration) 
        except ValueError:
             print(f"Warning: Invalid treatment duration '{treatment_duration}' for patient '{patient_id}'. Setting to default 0.")
             self.treatment_duration = 0
        
    def __str__(self):
        """Returns a string representation of the patient."""
        # Format duration for clarity
        duration_str = f"{self.treatment_duration} mins" if self.treatment_duration is not None else "N/A"
        return f"ID: {self.patient_id}, Name: {self.name}, Urgency: {self.urgency}, Condition: {self.condition}, Duration: {duration_str}"

class DSAHashEntry:
    """
    Container for each slot in the hash table array.
    Tracks the key, value, and the state of the slot.
    """
    def __init__(self, key=None, value=None):
        """Constructor for a hash table entry (slot)."""
        self.key = key       # The patient ID
        self.value = value   # The PatientRecord object
        self.state = 0       # 0=FREE, 1=USED, -1=PREVIOUSLY_USED

class DSAHashTable:
    """
    Hash table implementation using Open Addressing with Linear Probing.
    Stores PatientRecord objects, keyed by patient_id.
    """
    UPPER_THRESHOLD = 0.7  # Load factor to trigger resizing (growing)
    LOWER_THRESHOLD = 0.3  # Load factor to trigger resizing (shrinking)
    INITIAL_CAPACITY = 11  # Starting size (must be prime)

    def __init__(self, table_size=INITIAL_CAPACITY):
        """Constructor, initializes array and sets initial state."""
        actual_size = self._find_next_prime(table_size)
        # Initialize numpy array with None, then fill with DSAHashEntry objects
        self.hash_array = np.full(actual_size, None, dtype=object) 
        
        # Manually initialize each slot in the array with an empty entry
        i = 0
        while i < actual_size: 
            self.hash_array[i] = DSAHashEntry()
            i += 1
            
        self.count = 0        # Number of items currently in the table
        self.capacity = actual_size # Total number of slots

    def _hash(self, key):
        """
        Primary hash function (polynomial hash based on string characters).
        Converts the string key into an array index. Handles non-string keys gracefully.
        """
        hash_index = 0
        prime = 31 # A commonly used small prime for polynomial hashing
        
        # Convert key to string to handle potential non-string keys safely
        key_str = str(key) 

        i = 0
        while i < len(key_str): 
            # Use ASCII value of character
            hash_index = (hash_index * prime + ord(key_str[i])) % self.capacity
            i += 1
        return hash_index

    def _step_hash(self, key):
        """Step function for collision resolution. ALWAYS 1 for Linear Probing."""
        # Linear probing always steps by 1.
        return 1 

    def _find_next_prime(self, n):
        """Helper to find the next prime number >= n."""
        # Ensure n is at least 2
        num = max(2, int(n))
        
        # If even (and not 2), start checking from the next odd number
        if num > 2 and (num % 2) == 0:
            num += 1
            
        is_p = self._is_prime(num)
        # Keep checking subsequent odd numbers until a prime is found
        while not is_p:
            num += 2 # Check next odd number
            is_p = self._is_prime(num)
        return num


    def _is_prime(self, n):
        """Helper to check if a number is prime."""
        is_prime_flag = True # Assume prime initially
        if n <= 1: 
            is_prime_flag = False
        elif n == 2: 
            is_prime_flag = True # 2 is the only even prime
        elif (n % 2) == 0: 
            is_prime_flag = False # Other even numbers are not prime
        else:
            # Only check odd divisors up to the square root
            i = 3
            # Calculate integer part of square root
            max_divisor = int(math.sqrt(n)) 
            while is_prime_flag and i <= max_divisor:
                if (n % i) == 0: 
                    is_prime_flag = False # Found a divisor, not prime
                i += 2 # Check next odd number
        return is_prime_flag

    def get_load_factor(self):
        """Calculates the current load factor (items / slots)."""
        if self.capacity == 0: 
            return 0.0 # Avoid division by zero if capacity is somehow 0
        return self.count / self.capacity

    def insert(self, key, value):
        """
        Inserts a key-value pair using Linear Probing.
        Handles collisions and triggers resizing if needed. Rejects duplicate keys.
        """
        # 1. Resize if table is getting too full BEFORE insertion
        if self.get_load_factor() >= self.UPPER_THRESHOLD: 
            self._resize(is_growing=True)
            
        hash_index = self._hash(key)
        initial_index = hash_index
        step = self._step_hash(key)
        
        found_slot_index = -1 # Index where the item should be inserted
        first_deleted_slot = -1 # Keep track of the first deleted slot encountered
        
        probing = True
        while probing:
            entry = self.hash_array[hash_index]
            
            # Case 1: Slot is FREE (never used)
            if entry.state == 0:
                # If we passed a deleted slot, use that one; otherwise use this free slot
                found_slot_index = first_deleted_slot if first_deleted_slot != -1 else hash_index
                probing = False # Stop probing
            # Case 2: Slot is PREVIOUSLY_USED (deleted)
            elif entry.state == -1:
                # Record the first deleted slot we find
                if first_deleted_slot == -1:
                    first_deleted_slot = hash_index
                # Keep probing, the key might exist further down
            # Case 3: Slot is USED
            elif entry.state == 1:
                # Check if the keys match (duplicate)
                if entry.key == key:
                     print(f"Error: Key '{key}' already exists. Cannot insert duplicate.")
                     return # Do not insert duplicate, exit method
                # Keys don't match, collision occurred, continue probing
            
            # If we haven't stopped probing, calculate the next index
            if probing:
                hash_index = (hash_index + step) % self.capacity
                # Check if we've looped all the way around
                if hash_index == initial_index: 
                    # This should theoretically not happen if resizing works correctly
                    # but is a safeguard.
                    print("Error: Hash table is effectively full or looped unexpectedly.")
                    probing = False # Exit loop to prevent infinite loop
                    return # Indicate failure

        # If we successfully found a slot index to insert into
        if found_slot_index != -1:
             target_entry = self.hash_array[found_slot_index]
             target_entry.key = key
             target_entry.value = value
             target_entry.state = 1 # Mark as USED
             self.count += 1
             
    def get(self, key):
        """
        Retrieves the value for a key using Linear Probing.
        Raises KeyError if the key is not found.
        """
        hash_index = self._hash(key)
        initial_index = hash_index
        step = self._step_hash(key)
        
        found = False
        stop_searching = False # Flag to stop if we hit a truly FREE slot
        found_value = None
        
        # Probe until found, a FREE slot is hit, or we loop back
        while not found and not stop_searching:
            entry = self.hash_array[hash_index]
            
            # Case 1: Slot is FREE (never used) - Key cannot exist beyond this point
            if entry.state == 0:
                stop_searching = True 
            # Case 2: Slot is USED - Check if keys match
            elif entry.state == 1:
                if entry.key == key: 
                    found = True # We found the key
                    found_value = entry.value
            # Case 3: Slot is PREVIOUSLY_USED (-1) - Key might be further, continue probing
            
            # If not found and haven't hit a stop condition, probe next slot
            if not found and not stop_searching:
                hash_index = (hash_index + step) % self.capacity
                # Check if we've looped all the way around
                if hash_index == initial_index: 
                    stop_searching = True # Looped, key not found
                    
        # If the loop finished and the key was not found
        if not found: 
            raise KeyError(f"Key '{key}' not found in hash table.")
        return found_value

    def delete(self, key):
        """
        Deletes a key-value pair using Linear Probing.
        Sets the slot state to -1 (PREVIOUSLY_USED) instead of 0.
        Triggers shrinking resize if load factor falls below threshold.
        """
        hash_index = self._hash(key)
        initial_index = hash_index
        step = self._step_hash(key)
        
        found = False
        stop_searching = False
        deleted_value = None
        
        while not found and not stop_searching:
            entry = self.hash_array[hash_index]
            
            # Case 1: Slot is FREE - Key not found
            if entry.state == 0:
                stop_searching = True 
            # Case 2: Slot is USED - Check if keys match
            elif entry.state == 1:
                if entry.key == key:
                    found = True
                    deleted_value = entry.value
                    # Mark as PREVIOUSLY_USED (Tombstone)
                    entry.state = -1 
                    entry.key = None   # Clear key and value for garbage collection
                    entry.value = None
                    self.count -= 1
                   
            # Case 3: Slot is PREVIOUSLY_USED - Continue probing
            
            if not found and not stop_searching:
                hash_index = (hash_index + step) % self.capacity
                if hash_index == initial_index: 
                    stop_searching = True # Looped, key not found
                    
        if not found: 
            raise KeyError(f"Key '{key}' not found, cannot delete.")
            
        # 2. Resize (shrink) if table is too empty AFTER deletion
        # Only shrink if capacity is larger than the initial default
        if self.capacity > self.INITIAL_CAPACITY and self.get_load_factor() < self.LOWER_THRESHOLD: 
            self._resize(is_growing=False)
            
        return deleted_value

    def _resize(self, is_growing):
        """
        Resizes the hash table (grows or shrinks) and re-hashes all active elements.
        """
        old_capacity = self.capacity
        if is_growing: 
            new_capacity_suggestion = old_capacity * 2
        else:
            # Calculate potential shrink size, but don't go below initial capacity
            new_capacity_suggestion = max(self.INITIAL_CAPACITY, old_capacity // 2)

        # Find the next prime size >= the suggestion
        new_capacity = self._find_next_prime(new_capacity_suggestion)

        # Only proceed if the new size is actually different from the old size
        if new_capacity != old_capacity:
            print(f"Resizing hash table from {old_capacity} to {new_capacity}...")
            old_array = self.hash_array # Keep a reference to the old data
            
            # Create a new, empty array of the new capacity
            self.capacity = new_capacity
            self.hash_array = np.full(self.capacity, None, dtype=object)
            i = 0
            while i < self.capacity: 
                self.hash_array[i] = DSAHashEntry()
                i += 1
                
            self.count = 0 # Reset count, as 'insert' will increment it again
            
            # Re-hash all items from the old array into the new one
            i = 0
            while i < len(old_array):
                entry = old_array[i]
                if entry is not None and entry.state == 1: # Only re-hash USED items
                    # Use internal insert method which handles hashing for the new capacity
                    self.insert(entry.key, entry.value) 
                i += 1
            print(f"Resize complete. Current count: {self.count}")


    def read_patients_csv(self, filename):
        """Reads patient data from CSV and inserts into hash table.
           Uses boolean flags instead of continue.
        """
        try:
            # Use 'with' statement for safe file handling
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                # Use csv.reader for robust CSV parsing
                reader = csv.reader(csvfile)

                try:
                    header = next(reader) # Read and skip the header row
                    print(f"Loading patients from {filename}... Header: {header}")
                except StopIteration:
                     print("Warning: CSV file is empty or has no header.")
                     return # Nothing to load

                num_loaded = 0
                row_num = 1 # Start counting rows after header
                keep_reading = True

                while keep_reading:
                    try:
                        row = next(reader)
                        row_num += 1
                        process_row = False # Flag to determine if row should be processed

                        # Check if row has the expected number of columns (e.g., 4)
                        if len(row) == 4:
                            # Assumes 4-column CSV: ID, Name, Urgency, Condition
                            patient_id, name, urgency_str, condition = row[0], row[1], row[2], row[3]

                            # Validate and convert urgency
                            try:
                                urgency = int(urgency_str)
                                process_row = True # Mark row as potentially processable

                            except ValueError:
                                print(f"Skipping row {row_num}: Invalid urgency '{urgency_str}' for patient '{patient_id}'.")
                                
                        else:
                             print(f"Skipping row {row_num}: Malformed row, expected 4 columns, found {len(row)}. Content: {row}")                             

                        # Only insert if the row structure and urgency were valid
                        if process_row:
                            # Creates PatientRecord, treatment_duration defaults to 0
                            new_record = PatientRecord(patient_id, name, urgency, condition)
                            self.insert(patient_id, new_record)
                            num_loaded += 1
                       

                    except StopIteration:
                        keep_reading = False # End of file
                    except Exception as e: # Catch other potential errors during row processing
                         print(f"Error processing row {row_num}: {e}")
                         # Decide whether to keep_reading or stop based on error severity
                         # For now, we continue reading subsequent rows

                print(f"Successfully loaded {num_loaded} patients.")
        except FileNotFoundError:
            print(f"Error: File not found at '{filename}'")
        except Exception as e: # Catch errors opening or reading the file
            print(f"Error reading file '{filename}': {e}")



    def display(self):
        """Prints all USED entries currently in the hash table.
           Removed pass statement.
        """
        print("\n--- Current Patients in System (Hash Table) ---")
        i = 0
        found_any = False
        while i < self.capacity:
            entry = self.hash_array[i]
            if entry is not None and entry.state == 1: # If the slot is USED
                # Ensure value is a PatientRecord before printing details
                if isinstance(entry.value, PatientRecord):
                     print(f"  Index {i}: {entry.value}")
                else:
                     # Handle unexpected value types if necessary
                     print(f"  Index {i}: Key='{entry.key}', Value={entry.value} (Type: {type(entry.value).__name__})")
                found_any = True
            # No specific action needed for state == -1 or state == 0 when just displaying USED items
            i += 1

        if not found_any:
            print("  Hash table is currently empty.")

        print(f"Total Patients: {self.count} | Table Capacity: {self.capacity} | Load Factor: {self.get_load_factor():.2f}")
        print("-------------------------------------------------")

    
    def get_all_patients_as_list(self):
        """
        Extracts all active PatientRecord objects from the hash table
        into a standard Python list. Required input for sorting algorithms.
        """
        patient_list = []
        i = 0
        while i < self.capacity:
            entry = self.hash_array[i]
            # Check if entry exists and is in the USED state
            if entry is not None and entry.state == 1: 
                # Add the PatientRecord object (the value) to the list
                patient_list.append(entry.value) 
            i += 1
        return patient_list