# =================================================================
# File: module3_heap.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Implements a Max Heap data structure for the patient
#          triage priority queue. Includes DSATriageEntry and DSAHeap classes.
#          Heap implementation adapted from Practical 8.
# =================================================================

import numpy as np


class DSATriageEntry:
    """
    Container for heap entries. Holds the calculated priority score
    and the full PatientRecord object associated with that score.
    """
    def __init__(self, priority_score, patient_record):
        """Constructor for a triage queue entry."""
        # Validate inputs if necessary
        if not isinstance(priority_score, (int, float)):
             raise TypeError("priority_score must be a number.")
        
        self.priority_score = priority_score
        self.patient_record = patient_record # Should be a PatientRecord object

    def __str__(self):
        """Returns a string representation of the triage entry."""
        # Use f-string for cleaner formatting, format priority score
        return f"Priority: {self.priority_score:.2f} | Patient: {self.patient_record}"

class DSAHeap:
    """
    A Max-Heap implementation (using a numpy array) for the
    patient triage priority queue. Stores DSATriageEntry objects.
    """
    DEFAULT_CAPACITY = 100 # Default size if none is provided

    def __init__(self, max_size=DEFAULT_CAPACITY):
        """Constructor, initializes numpy array for the heap."""
        if not isinstance(max_size, int) or max_size <= 0:
            print(f"Warning: Invalid max_size '{max_size}'. Using default capacity {self.DEFAULT_CAPACITY}.")
            max_size = self.DEFAULT_CAPACITY

        # Initialize array with None to hold DSATriageEntry objects
        self.heap = np.full(max_size, None, dtype=object)
        self.count = 0 # Number of items currently in the heap
        self.capacity = max_size # Store capacity

    def get_count(self):
        """Returns the current number of items in the heap."""
        return self.count

    def is_empty(self):
         """Checks if the heap is empty."""
         return self.count == 0

    def is_full(self):
         """Checks if the heap is full."""
         return self.count >= self.capacity

    def insert(self, entry):
        """Adds a DSATriageEntry to the heap and maintains heap property."""
        if self.is_full():
            raise OverflowError("Triage Heap is full. Cannot insert.")
        if not isinstance(entry, DSATriageEntry):
             raise TypeError("Can only insert DSATriageEntry objects into the heap.")

        print(f"\nAdding to triage: {entry}")
        # Add entry to the next available slot (end of the current heap)
        self.heap[self.count] = entry
        self.count += 1
        # Restore heap property by moving the new element up
        self._trickle_up(self.count - 1)
        print("...Add complete.")

    def extract_next(self):
        """
        Removes and returns the highest priority DSATriageEntry (the root).
        Maintains the heap property after removal.
        """
        if self.is_empty():
            raise IndexError("Triage Heap is empty. Cannot extract.")

        print("\nTriaging next patient...")
        # The root element has the highest priority in a max-heap
        next_patient_entry = self.heap[0]

        # Get the last element in the heap
        last_item_index = self.count - 1
        last_item = self.heap[last_item_index]

        # Move the last element to the root position
        self.heap[0] = last_item
        # Clear the original spot of the last element
        self.heap[last_item_index] = None
        # Decrease the count since an element was removed
        self.count -= 1

        # Restore heap property starting from the new root (if heap not empty)
        if self.count > 0:
            self._trickle_down(0)

        print(f"...Triage complete. Next patient: {next_patient_entry}")
        return next_patient_entry

    def _trickle_up(self, index):
        """
        Moves an item UP the heap from the given index to maintain the Max-Heap property.
        An item moves up if its priority score is LARGER than its parent's score.
        Uses a while loop without break/continue/pass.
        """
        parent_index = (index - 1) // 2
        # Loop condition combines the checks: not root AND child > parent
        keep_trickling = (index > 0 and
                          self.heap[index].priority_score > self.heap[parent_index].priority_score)

        while keep_trickling:
            print(f"  HEAP LOG (Trickle Up): Swapping [idx {index}] (Prio {self.heap[index].priority_score:.2f}) with Parent [idx {parent_index}] (Prio {self.heap[parent_index].priority_score:.2f})")

            # Swap the current node with its parent
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]

            # Move up to the parent's index for the next potential iteration
            index = parent_index
            parent_index = (index - 1) // 2

            # Re-evaluate loop condition for the new position
            keep_trickling = (index > 0 and
                              self.heap[index].priority_score > self.heap[parent_index].priority_score)


    def _trickle_down(self, index):
        """
        Moves an item DOWN the heap from the given index to maintain the Max-Heap property.
        An item moves down by swapping with its LARGEST child if the child's priority is greater.
        Uses a while loop with a flag, avoiding break/continue/pass.
        """
        # Flag to control the loop
        is_trickling = True

        while is_trickling:
            left_child_idx = 2 * index + 1
            right_child_idx = 2 * index + 2
            largest_idx = index # Assume the current node is the largest initially

            # Check if left child exists within the heap boundary
            # AND if left child's priority is greater than the current largest's priority
            if left_child_idx < self.count and self.heap[left_child_idx].priority_score > self.heap[largest_idx].priority_score:
                largest_idx = left_child_idx

            # Check if right child exists within the heap boundary
            # AND if right child's priority is greater than the current largest's priority
            if right_child_idx < self.count and self.heap[right_child_idx].priority_score > self.heap[largest_idx].priority_score:
                largest_idx = right_child_idx

            # If the largest priority belongs to one of the children (not the current node)
            if largest_idx != index:
                print(f"  HEAP LOG (Trickle Down): Swapping [idx {index}] (Prio {self.heap[index].priority_score:.2f}) with Largest Child [idx {largest_idx}] (Prio {self.heap[largest_idx].priority_score:.2f})")

                # Swap the current node with its largest child
                self.heap[index], self.heap[largest_idx] = self.heap[largest_idx], self.heap[index]

                # Move down to the child's index for the next iteration
                index = largest_idx
                # Continue trickling from the new position (is_trickling remains True)
            else:
                # If the current node is larger than or equal to both children,
                # the heap property is satisfied at this position, so stop.
                is_trickling = False # Set the flag to False to exit the loop


    def display(self):
        """Prints the current heap array contents for visualization."""
        print("\n--- Current Triage Queue (Heap Array) ---")
        if self.is_empty():
            print("  Queue is empty.")
        else:
            i = 0
            # Iterate only up to the current count of items
            while i < self.count:
                 # Ensure the element is not None before printing (safety check)
                 if self.heap[i] is not None:
                      print(f"  Index {i}: {self.heap[i]}")
                 else:
                      # This shouldn't happen if count is managed correctly
                      print(f"  Index {i}: <Unexpected None>")
                 i += 1
        print(f"Total Patients in Queue: {self.count} | Capacity: {self.capacity}")
        print("-------------------------------------------")