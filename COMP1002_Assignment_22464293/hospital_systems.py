# =================================================================
# File: hospital_system.py
# Author: [Your Name]
# ID: [Your ID]
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Main application file for the Hospital Management System.
#          Imports all necessary modules (Graph, Hash Table, Heap, Sorts)
#          and runs the interactive command-line menu.
# =================================================================

# --- Imports (Combined for all modules) ---
import timeit    # For timing sorting algorithms
import random    # For generating test data

# --- Import from custom module files ---
from dsa_linked_list import DSALinkedList # Base data structure
from dsa_stacks_queues import DSAStack, DSAQueue # Used by Graph algorithms
from module1_graph import DSAGraphNode, DSAGraph # Module 1 components
from module2_hash_table import PatientRecord, DSAHashTable # Module 2 components 
from module3_heap import DSATriageEntry, DSAHeap # Module 3 components
from module4_sorts import mergeSort, quickSort # Module 4 sorting functions

# =================================================================
# == MODULE 4: BENCHMARKING (Stays in the main file)
# =================================================================

REPEATS = 3 # Number of times to repeat each sort for timing average

def _generate_test_patient_list(size, condition='random'):
    """
    Helper function to generate lists of PatientRecord objects for benchmarking Module 4.
    Creates lists where 'treatment_duration' attribute follows the specified condition
    (random, sorted, or reverse). Urgency is random (1-5).
    """
    test_list = []
    
    # Generate the sequence of treatment durations based on the condition
    if condition == 'random':
        # Generate unique durations between 5 and a larger upper bound to ensure uniqueness
        upper_bound = 5 + size * 2 
        durations = random.sample(range(5, upper_bound), size) 
    elif condition == 'sorted':
        # Durations ascending from 5 (e.g., 5, 6, 7...)
        durations = list(range(5, 5 + size))
    elif condition == 'reverse':
        # Durations descending from (5 + size - 1) down to 5 (e.g., 104, 103...)
        durations = list(range(5 + size - 1, 4, -1)) # Stop at 5 (index 4 is exclusive)
    else: 
        # Default to random if condition is unrecognized
        print(f"Warning: Unrecognized condition '{condition}'. Generating random data.")
        upper_bound = 5 + size * 2 
        durations = random.sample(range(5, upper_bound), size) 
        
    # Create PatientRecord objects using the generated durations
    i = 0
    while i < size:
        # Generate unique patient ID for testing purposes
        p_id = f"BENCH{10000 + i}" 
        name = f"Benchmark Patient {i}"
        # Generate random urgency according to the required 1-5 scale
        urgency = random.randint(1, 5) 
        cond = "Benchmark Condition"
        # Get the duration for this patient from the generated list
        duration = durations[i] 
        
        # Create the PatientRecord object
        test_list.append(PatientRecord(p_id, name, urgency, cond, duration))
        i += 1
        
    return test_list

def run_performance_comparison():
    """
    Runs Merge Sort and Quick Sort (all 3 pivots) on generated datasets
    of different sizes and conditions. Times the execution using timeit
    and prints a formatted table summarizing the average results.
    """
    # Define test scenarios
    sizes = [100, 500, 1000] # Dataset sizes to test
    conditions = ['random', 'sorted', 'reverse'] # Input data conditions
    
    # Define algorithms to test: Name mapped to the statement string for timeit
    algorithms = {
        'Merge Sort': 'mergeSort(list_copy)', 
        'Quick Sort (Left)': "quickSort(list_copy, pivot_mode='left')",
        'Quick Sort (Median3)': "quickSort(list_copy, pivot_mode='median3')",
        'Quick Sort (Random)': "quickSort(list_copy, pivot_mode='random')"
    }
    
    results = [] # List to store tuples of (algo_name, size, condition, avg_time_str)

    print("\n--- Running Sorting Performance Comparison ---")
    print(f"(Timing based on average of {REPEATS} runs per scenario)")

    # Iterate through each combination of size and condition
    size_idx = 0
    while size_idx < len(sizes):
        size = sizes[size_idx]
        cond_idx = 0
        while cond_idx < len(conditions):
            condition = conditions[cond_idx]
            print(f"\nGenerating {condition} data (Size: {size})...")
            # Create the master list for this specific scenario
            original_list = _generate_test_patient_list(size, condition)
            
            # Test each defined algorithm on this list
            algo_names = list(algorithms.keys()) # Get algorithm names
            algo_idx = 0
            while algo_idx < len(algo_names):
                 algo_name = algo_names[algo_idx]
                 stmt_str = algorithms[algo_name] # Get the timeit statement string

                 print(f"  Timing {algo_name}...")
                 total_time = 0.0
                 num_valid_runs = 0
                 error_occurred = False # Flag to track if any run failed

                 # Repeat the timing multiple times for a more stable average
                 repeat_count = 0
                 while repeat_count < REPEATS and not error_occurred:
                    
                     # Setup string for timeit: imports functions and creates list_copy
                     # list_copy must be created inside setup or stmt for each run
                     setup_str = f"""
from __main__ import mergeSort, quickSort 
# Access original_list from globals passed to Timer
list_copy = list(original_list) 
"""
                    
                     try:
                         # Create a dictionary of globals needed by setup/stmt
                         timer_globals = globals().copy()
                         timer_globals['original_list'] = original_list # Make original_list accessible

                         # Create Timer object
                         timer = timeit.Timer(stmt=stmt_str, setup=setup_str, globals=timer_globals)
                         
                         # Execute the statement once and measure time
                         time_taken = timer.timeit(number=1) 
                         
                         total_time += time_taken
                         num_valid_runs += 1
                         
                     except RecursionError:
                         # Mark result as RecursionError and stop repeats for this algo/condition
                         total_time = -1.0 
                         num_valid_runs = 1 # To avoid division by zero later
                         error_occurred = True # Stop further repeats for this case
                     except Exception as e:
                         # Catch other potential errors during timing
                         print(f"    Unexpected error during timing: {e}")
                         total_time = -2.0 # Indicate a different error
                         num_valid_runs = 1
                         error_occurred = True # Stop further repeats for this case
                     
                     repeat_count += 1 

                 # Calculate average time string based on results
                 if total_time == -1.0:
                     avg_time_str = "RecursionError"
                 elif total_time == -2.0:
                     avg_time_str = "TimingError"
                 elif num_valid_runs > 0:
                     # Calculate average time if runs were successful
                     avg_time = total_time / num_valid_runs
                     avg_time_str = f"{avg_time:.6f}" # Format to 6 decimal places
                 else: 
                      # Should not happen if REPEATS >= 1, but handles edge case
                      avg_time_str = "N/A" 
                      
                 # Store the result for this algorithm/size/condition
                 results.append((algo_name, size, condition, avg_time_str))
                 algo_idx += 1 # Move to next algorithm
            cond_idx += 1 # Move to next condition
        size_idx += 1 # Move to next size


    # --- Print the final Results Table ---
    print("\n--- Performance Comparison Results (Average Time in Seconds) ---")
    # Print header row
    print(f"{'Algorithm':<25} | {'Size':<6} | {'Condition':<10} | {'Avg Time (s)':<15}")
    print("-" * 65) # Separator line
    # Print each result row stored in the results list
    i = 0
    while i < len(results):
        algo, sz, cond, time_str = results[i]
        print(f"{algo:<25} | {sz:<6} | {cond:<10} | {time_str:<15}")
        i += 1
    print("-" * 65) # Footer separator line
    print("---------------------------------------------------------------")


# =================================================================
# == Main execution block: Setup and Interactive Menu
# =================================================================
if __name__ == "__main__":
    # This block runs only when the script is executed directly
    
    # --- Module 1 Setup: Initialize Graph and add sample data ---
    my_graph = DSAGraph()
    print("Graph system initializing...")
    # List of departments (nodes)
    departments = ['Emergency', 'ICU', 'Pharmacy', 'Radiology', 'Labs', 
                   'Operating Theatres', 'Wards', 'Outpatient', 'Admin'] # Added Admin here
    
    # Add vertices to the graph
    i = 0
    while i < len(departments):
        my_graph.add_vertex(departments[i])
        i += 1
        
    # Add edges (corridors) with weights (walking times)
    # Ensures undirected edges are added correctly
    my_graph.add_edge('Emergency', 'ICU', 2)
    my_graph.add_edge('Emergency', 'Radiology', 3)
    my_graph.add_edge('Emergency', 'Operating Theatres', 4)
    my_graph.add_edge('ICU', 'Operating Theatres', 2)
    my_graph.add_edge('ICU', 'Wards', 5)
    my_graph.add_edge('Radiology', 'Labs', 2)
    my_graph.add_edge('Labs', 'Pharmacy', 1)
    my_graph.add_edge('Operating Theatres', 'Wards', 3)
    my_graph.add_edge('Wards', 'Outpatient', 4)
    my_graph.add_edge('Outpatient', 'Pharmacy', 3)
    # This edge creates a cycle involving Labs, Wards, and potentially others
    my_graph.add_edge('Labs', 'Wards', 5) 
    print("Sample hospital graph loaded.")
    
    # --- Module 2 Setup: Initialize Hash Table and load initial data ---
    my_patient_table = DSAHashTable() # Use default initial capacity
    print("Patient lookup system initializing...")
    # Attempt to load initial patients from 'patients.csv'
    # Ensure this file exists in the same directory or provide the correct path
    my_patient_table.read_patients_csv('patients.csv') 
    
    # --- Module 3 Setup: Initialize Triage Heap ---
    # Set a reasonable maximum size for the triage queue
    my_triage_queue = DSAHeap(max_size=100) 
    print("Triage priority queue initializing...")

    # --- Main Menu Loop ---
    running = True # Flag to control the main loop
    while running:
        # Display the main menu options clearly grouped by module
        print("\n--- Hospital Management System Menu ---")
        print("--- Module 1: Graph Operations ---")
        print(" 1. Display Adjacency List")
        print(" 2. Display Adjacency Matrix")
        print(" 3. Run BFS (Grouped by Level)")
        print(" 4. Run DFS (Detect Cycles)")
        print(" 5. Find Shortest Path (Dijkstra's)")
        print("--- Module 2: Patient Lookup ---")
        print(" 10. Add New Patient")
        print(" 11. Find Patient by ID")
        print(" 12. Delete Patient by ID")
        print(" 13. Display All Patients (Hash Table)")
        print(" 14. Re-load Patients from CSV (Clears current table)")
        print("--- Module 3: Triage Queue ---")
        print(" 20. Add Patient to Triage Queue")
        print(" 21. Triage Next Patient")
        print(" 22. Display Triage Queue")
        print("--- Module 4: Sorting ---")
        print(" 30. Sort Current Patients (Merge Sort - by Duration)")
        print(" 31. Sort Current Patients (Quick Sort - by Duration)")
        print(" 32. Run Sorting Performance Comparison")
        print("---------------------------------")
        print(" 0. Exit")
        choice = input("Enter your choice: ").strip() # Get user input and remove whitespace

        # --- Process User Choice ---
        
        # --- Module 1 Choices ---
        if choice == '1': 
            my_graph.display_as_list()
            
        elif choice == '2': 
            my_graph.display_as_matrix()
            
        elif choice == '3': 
            label = input("Enter start department for BFS: ").strip()
            # Check if vertex exists before running BFS
            if my_graph.get_vertex(label):
                 my_graph.breadth_first_search_by_level(label)
            else:
                 print(f"Error: Department '{label}' not found.")
            
        elif choice == '4': 
            label = input("Enter start department for DFS cycle check: ").strip()
             # Check if vertex exists before running DFS
            if my_graph.get_vertex(label):
                 my_graph.depth_first_search_cycle_detect(label)
            else:
                 print(f"Error: Department '{label}' not found.")

        elif choice == '5': 
            l1 = input("Enter start department: ").strip()
            l2 = input("Enter destination department: ").strip()
            # Check if both vertices exist before finding path
            if my_graph.get_vertex(l1) and my_graph.get_vertex(l2):
                 my_graph.find_shortest_path(l1, l2)
            else:
                 if not my_graph.get_vertex(l1): print(f"Error: Start department '{l1}' not found.")
                 if not my_graph.get_vertex(l2): print(f"Error: Destination department '{l2}' not found.")
        
        # --- Module 2 Choices ---
        elif choice == '10':
            print("--- Add New Patient ---")
            try:
                # Get patient details from user
                p_id = input("Enter Patient ID: ").strip()
                p_name = input("Enter Patient Name: ").strip()
                # Use the required 1-5 urgency scale
                urgency_str = input("Enter Urgency (1=High, 5=Low): ").strip()
                p_urgency = int(urgency_str) # Convert to integer
                p_condition = input("Enter Condition: ").strip()
                
                # Input validation
                if not p_id: print("Error: Patient ID cannot be empty.")
                elif not p_name: print("Error: Patient Name cannot be empty.")
                elif not (1 <= p_urgency <= 5): 
                    print("Error: Urgency must be an integer between 1 and 5.")
                elif not p_condition: print("Error: Condition cannot be empty.")
                else: 
                    # Create PatientRecord (duration defaults to 0)
                    new_record = PatientRecord(p_id, p_name, p_urgency, p_condition)
                    # Insert into hash table (handles duplicates check internally)
                    my_patient_table.insert(p_id, new_record)
                    # Confirmation message managed within insert if successful/duplicate
            except ValueError: 
                print("Error: Urgency must be a valid integer.")
            except Exception as e: # Catch unexpected errors
                print(f"An unexpected error occurred: {e}")
                
        elif choice == '11':
            print("--- Find Patient ---")
            p_id = input("Enter Patient ID to find: ").strip()
            if not p_id: 
                 print("Error: Patient ID cannot be empty.")
            else:
                 try: 
                      # Attempt to retrieve patient record from hash table
                      record = my_patient_table.get(p_id)
                      print(f"Found: {record}")
                 except KeyError as e: # Handle case where key is not found
                      print(e) 
                
        elif choice == '12':
            print("--- Delete Patient ---")
            p_id = input("Enter Patient ID to delete: ").strip()
            if not p_id:
                 print("Error: Patient ID cannot be empty.")
            else:
                 try: 
                      # Attempt to delete patient record from hash table
                      record = my_patient_table.delete(p_id)
                      print(f"Deleted: {record}")
                 except KeyError as e: # Handle case where key is not found
                      print(e)
                
        elif choice == '13': 
            # Display current contents of the hash table
            my_patient_table.display()
            
        elif choice == '14': 
            print("Re-loading patients from 'patients.csv'...")
            # Re-initialize the hash table (clears existing data)
            my_patient_table = DSAHashTable()
            # Load data from the CSV file again
            my_patient_table.read_patients_csv('patients.csv')
            print("Patient data re-loaded.")

        # --- Module 3 Choices ---
        elif choice == '20':
            print("--- Add Patient to Triage Queue ---")
            try:
                # 1. Get Patient ID and retrieve record from hash table
                p_id = input("Enter Patient ID to add to triage: ").strip()
                if not p_id: raise ValueError("Patient ID cannot be empty.")
                
                patient = my_patient_table.get(p_id) # Raises KeyError if not found
                
                # 2. Validate patient's urgency is within the required 1-5 range
                if not (1 <= patient.urgency <= 5):
                    print(f"Error: Patient '{p_id}' has an invalid urgency ({patient.urgency}). Must be between 1 and 5.")
                else:
                    print(f"Found Patient: {patient.name}, Urgency: {patient.urgency} (1=High, 5=Low)")
                    
                    # 3. Get expected treatment time from user
                    time_str = input("Enter expected treatment time (in minutes): ").strip()
                    treatment_time = int(time_str) # Raises ValueError if not integer
                    
                    # 4. Validate treatment time (must be positive for formula)
                    if treatment_time <= 0: 
                        print("Error: Treatment time must be a positive number (greater than 0).")
                    else:
                        # 5. Update the patient record in the hash table with this duration
                        #    This allows Module 4 sorting to use the assigned time
                        patient.treatment_duration = treatment_time
                        
                        # 6. Calculate priority score using the formula 
                        # Priority = (6 - U) + 1000 / T 
                        priority_score = (6 - patient.urgency) + (1000 / treatment_time)
                        
                        # 7. Create a DSATriageEntry object
                        triage_entry = DSATriageEntry(priority_score, patient)
                        
                        # 8. Insert the entry into the heap (triage queue)
                        my_triage_queue.insert(triage_entry)
                    
            except KeyError: # Catch error if patient ID not found in hash table
                print(f"Error: Patient ID '{p_id}' not found in the system.") 
            except ValueError: # Catch error if treatment time is not a valid integer
                print("Error: Invalid input. Treatment time must be an integer.")
            except ZeroDivisionError: # Should be caught by time validation, but good practice
                print("Error: Treatment time cannot be zero.")
            except OverflowError as e: # Catch error if heap is full
                 print(e)
            except Exception as e: # Catch any other unexpected errors
                print(f"An unexpected error occurred: {e}") 
                
        elif choice == '21':
            print("--- Triage Next Patient ---")
            try: 
                # Attempt to extract the patient with the highest priority from the heap
                next_patient_entry = my_triage_queue.extract_next()
                print(f"\n===> NEXT PATIENT TO TREAT: {next_patient_entry} <===")
            except IndexError as e: # Catch error if heap is empty
                print(e) 
            except Exception as e: # Catch other potential errors
                 print(f"An error occurred during triage: {e}")
                
        elif choice == '22': 
            # Display the current state of the triage heap
            my_triage_queue.display()

        # --- Module 4 Choices ---
        elif choice == '30':
            print("\n--- Sorting Current Patients (Merge Sort by Duration) ---")
            # 1. Retrieve all current patients from the hash table as a list
            current_patients = my_patient_table.get_all_patients_as_list()
            
            if len(current_patients) == 0:
                print("No patients currently in the system to sort.")
            else:
                # 2. Perform Merge Sort (returns a new sorted list)
                print(f"Sorting {len(current_patients)} patients...")
                # It's good practice to time even the live sorts for user feedback
                start_time = timeit.default_timer()
                try:
                    sorted_list_ms = mergeSort(current_patients) # Pass the original list
                    end_time = timeit.default_timer()
                    time_taken_ms = end_time - start_time
                    
                    # 3. Print the sorted list
                    print("Sorted List (by Treatment Duration Ascending):")
                    i = 0
                    while i < len(sorted_list_ms): 
                        print(f"  {sorted_list_ms[i]}")
                        i += 1
                    print(f"\nMerge Sort completed in {time_taken_ms:.6f} seconds.")
                except Exception as e:
                    print(f"An error occurred during Merge Sort: {e}")
            print("-----------------------------------------------------")
            
        elif choice == '31':
            print("\n--- Sorting Current Patients (Quick Sort by Duration) ---")
            # 1. Retrieve all current patients
            current_patients = my_patient_table.get_all_patients_as_list()
            
            if len(current_patients) == 0:
                print("No patients currently in the system to sort.")
            else:
                # 2. Create a copy because Quick Sort modifies the list in-place
                list_to_sort_qs = list(current_patients) 
                print(f"Sorting {len(list_to_sort_qs)} patients using Quick Sort (Median-of-Three)...")
                
                start_time = timeit.default_timer()
                try:
                    # 3. Perform Quick Sort (using the default 'median3' pivot)
                    quickSort(list_to_sort_qs, pivot_mode='median3') 
                    end_time = timeit.default_timer()
                    time_taken_qs = end_time - start_time
                    
                    # 4. Print the sorted list (which is list_to_sort_qs)
                    print("Sorted List (by Treatment Duration Ascending):")
                    i = 0
                    while i < len(list_to_sort_qs): 
                        print(f"  {list_to_sort_qs[i]}")
                        i += 1
                    print(f"\nQuick Sort (Median-of-Three) completed in {time_taken_qs:.6f} seconds.")
                except RecursionError:
                     # This shouldn't happen with median3 unless list is pathologically large/structured
                     print("ERROR: Quick Sort hit recursion limit. Sorting aborted.")
                except Exception as e:
                    print(f"An error occurred during Quick Sort: {e}")
            print("-------------------------------------------------------")
            
        elif choice == '32':
            # Execute the detailed performance comparison benchmark
            run_performance_comparison()

        # --- Exit Option ---
        elif choice == '0':
            print("Exiting Hospital Management System. Goodbye.")
            running = False # Set flag to terminate the main while loop
        
        # --- Invalid Input Handling ---
        else:
            print("Invalid choice. Please enter a number from the menu (0-32).")