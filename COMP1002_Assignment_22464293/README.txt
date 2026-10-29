COMP1002 Data Structures and Algorithms - Final Assignment
Critical Care Optimisation: Data Structures and Algorithms for Hospital Efficiency
Student Name: Tushar Pirwani
Student ID: 22464293

Project Overview:
This project implements a modular hospital resource management system demonstrating the application of core data structures and algorithms covered in COMP1002. The system simulates hospital operations including department navigation, patient record lookup, emergency case scheduling, and patient record sorting.

The system is divided into four main functional modules, supported by base data structures:
Module 1: Graph-based navigation using Adjacency Lists, BFS, DFS, and Dijkstra's.
Module 2: Hash Table for patient record storage and lookup using Linear Probing.
Module 3: Max Heap for priority queue implementation based on urgency and treatment time.
Module 4: Merge Sort and Quick Sort (with multiple pivot strategies) for sorting patient records by treatment duration and performance benchmarking.

Files Included
The submission includes the following Python files:
1. hospital_system.py: The main application script that runs the interactive menu and orchestrates module interactions. Contains the Module 4 benchmarking code.
2. module1_graph.py: Contains the DSAGraphNode and DSAGraph classes and related algorithms (BFS, DFS, Dijkstra's).
3. module2_hash_table.py: Contains the PatientRecord, DSAHashEntry, and DSAHashTable classes.
4. module3_heap.py: Contains the DSATriageEntry and DSAHeap classes.
5. module4_sorts.py: Contains the mergeSort and quickSort implementations.
6. dsa_linked_list.py: Base implementation of a Doubly Linked List.
7. dsa_stacks_queues.py: Stack and Queue implementations using the Doubly Linked List.
And the following supporting files:
1. patients.csv: Sample input data file containing initial patient records.
2. Technical_report_DSA.pdf: The technical report detailing the project implementation and analysis.
3. README.txt (this file): Instructions for running and testing the system.

Dependencies
Python 3 (Developed and tested with Python 3)
numpy library (Used for array creation in Hash Table and Heap modules). 

How to Run
Ensure Python 3 and numpy are installed.
Place all .py files and the patients.csv file in the same directory.
Open a terminal or command prompt in that directory.
Run the main script using the command:
python3 hospital_system.py


The program will initialize, load the sample graph and patient data, and display the main menu.
Enter the number corresponding to the desired menu option and follow the prompts.

How to Test Each Module
Use the interactive menu options to test the functionality corresponding to each module's requirements:

Module 1: Graph-Based Hospital Navigation

Graph Construction & Display:
Option 1: Display Adjacency List (shows structure and weights).
Option 2: Display Adjacency Matrix (shows structure and weights) # not required by assignment, i just have it from my practical code.
(The graph is pre-loaded with the required test case: 8+ departments, 10+ edges, a cycle, and an isolated node 'Admin').

BFS (Breadth-First Search):
Option 3: Run BFS (Grouped by Level). Enter a starting department (e.g., Emergency). Output shows reachable departments grouped by hops.

DFS (Depth-First Search) Cycle Detection:
Option 4: Run DFS (Detect Cycles). Enter a starting department (e.g., Labs). Output indicates if a cycle is found and the back edge involved.

Shortest Path (Dijkstra's Algorithm):
Option 5: Find Shortest Path. Enter a start and end department (e.g., Emergency, Pharmacy). Output shows the path and total time. Test with the isolated node 'Admin' to show no path.


Module 2: Hash-Based Patient Lookup

Loading & Display:
The system automatically loads patients.csv on startup (demonstrates loading 20+ records and resizing).
Option 13: Display All Patients (Hash Table). Shows current records, count, capacity, and load factor.

Core Operations:
Option 10: Add New Patient. Enter details (ensures Urgency is 1-5). Test adding duplicates (should fail).
Option 11: Find Patient by ID. Test finding existing patients (e.g., P10001) and non-existent patients (e.g., P999).
Option 12: Delete Patient by ID. Test deleting an existing patient (e.g., P10001) and verify by searching again (should fail). Observe count decrease.

Collision Handling & Resizing: Demonstrated implicitly by loading 20 records into a table starting at size 11, forcing collisions and triggering resizing (output shown on startup). Further insertions/deletions may trigger resizing if thresholds are met.


Module 3: Heap-Based Emergency Scheduling

Integration & Priority Calculation:
Option 10: Add test patients with Urgency 1-5 (e.g., P1 U=1, P2 U=3, P3 U=5).
Option 20: Add Patient to Triage Queue. Use the test patients (P1, P2, P3) and provide positive treatment times (e.g., T=50, T=20, T=80). Observe the "Adding to triage..." message showing the calculated priority score based on the formula (6-U) + 1000/T. Test adding patients from CSV with urgency > 5 (should fail validation). Test adding with T<=0 (should fail validation).

Heap Operations & Tracing:
Observe the "HEAP LOG (Trickle Up)..." messages during Option 20 insertions.
Option 22: Display Triage Queue. Shows the heap array state after insertions, verifying the Max Heap property (highest score at index 0).
Option 21: Triage Next Patient. Observe the "HEAP LOG (Trickle Down)..." messages. The output shows the highest priority patient being extracted.
Use Option 22 again after extraction to verify the heap property is maintained.
Test Option 21 on an empty queue (should show error).

Module 4: Sorting Patient Records

Correctness (Sort by Duration):
Use Option 20 to assign different treatment_duration values to a few patients (e.g., P1=50, P2=20, P3=80). Other patients loaded from CSV will have duration 0.
Option 30: Sort Current Patients (Merge Sort). Verify the output list is sorted primarily by duration (0s first, then 20, 50, 80).
Option 31: Sort Current Patients (Quick Sort - Median3). Verify the output list is also sorted correctly by duration.

Performance Benchmark:
Option 32: Run Sorting Performance Comparison. This runs tests on generated lists (sizes 100, 500, 1000; conditions random, sorted, reverse). Observe the final output table. Verify that Quick Sort (Left) shows RecursionError for sorted/reverse data at size 1000, while other algorithms complete successfully, demonstrating the performance differences.

Input Data
patients.csv: A comma-separated value file. Expected format:
PatientID,Name,Urgency,Condition
P10001,John Smith,8,Broken Arm







