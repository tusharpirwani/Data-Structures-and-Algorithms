# =================================================================
# File: module4_sorts.py
# Author: Tushar Pirwani
# ID: 22464293
# Unit: COMP1002 Data Structures and Algorithms
# Purpose: Provides implementations of Merge Sort and Quick Sort
#          (with multiple pivot strategies) for sorting PatientRecord objects.
#          Sorting algorithms adapted from Practical 9.
# =================================================================

import random

# --- Merge Sort Implementation ---

def mergeSort(patient_list):
    """
    Initiates Merge Sort on a list of PatientRecord objects.
    Sorts based on the 'treatment_duration' attribute in ascending order.
    Returns a NEW sorted list, the original list remains unmodified.
    """
    # Create a copy to avoid modifying the original list passed to the function
    list_copy = list(patient_list)

    # Base case: A list with 0 or 1 element is already sorted.
    if len(list_copy) <= 1:
        return list_copy
    else:
        # 1. Divide: Find the midpoint index.
        midIdx = len(list_copy) // 2
        
        # 2. Conquer: Recursively sort the left and right halves.
        #    Use list slicing to create sub-lists for recursion.
        left_half = mergeSort(list_copy[0:midIdx])
        right_half = mergeSort(list_copy[midIdx:len(list_copy)])
        
        # 3. Combine: Merge the two sorted halves.
        return _merge(left_half, right_half)

def _merge(left_list, right_list):
    """
    Helper for Merge Sort. Merges two sorted lists of PatientRecord objects
    into a single sorted list based on 'treatment_duration'.
    """
    merged_list = [] # The list to build the sorted result
    left_idx = 0     # Pointer for the left list
    right_idx = 0    # Pointer for the right list

    # Compare elements from both lists and append the smaller one
    while left_idx < len(left_list) and right_idx < len(right_list):
        # Comparison based on 'treatment_duration'
        # Ensure objects are PatientRecord instances before accessing attribute (optional check)
        if isinstance(left_list[left_idx], object) and hasattr(left_list[left_idx], 'treatment_duration') and \
           isinstance(right_list[right_idx], object) and hasattr(right_list[right_idx], 'treatment_duration'):
             
             if left_list[left_idx].treatment_duration <= right_list[right_idx].treatment_duration:
                 merged_list.append(left_list[left_idx])
                 left_idx += 1
             else:
                 merged_list.append(right_list[right_idx])
                 right_idx += 1
        else:
             # Handle cases where items might not be PatientRecord objects if necessary
             # For this context, we assume the list contains valid objects
             # Raise an error or log a warning if needed
             raise TypeError("List contains items without 'treatment_duration' attribute.")


    # Append any remaining elements from the left list
    while left_idx < len(left_list):
        merged_list.append(left_list[left_idx])
        left_idx += 1
        
    # Append any remaining elements from the right list
    while right_idx < len(right_list):
        merged_list.append(right_list[right_idx])
        right_idx += 1

    return merged_list

# --- Quick Sort Implementation ---

def _median_of_three(A, leftIdx, rightIdx):
    """
    Helper for Quick Sort: Selects pivot index using Median-of-Three strategy.
    Compares 'treatment_duration' of left, middle, and right elements.
    Returns the index of the median element.
    """
    midIdx = (leftIdx + rightIdx) // 2
    
    # Ensure indices are valid before accessing elements
    if not (leftIdx < len(A) and midIdx < len(A) and rightIdx < len(A)):
         # Handle potential index out of bounds, though unlikely if called correctly
         # Default to left index as a fallback
         return leftIdx

    left_val = A[leftIdx]
    mid_val = A[midIdx]
    right_val = A[rightIdx]
    
    # Check if elements are valid PatientRecord objects (optional safety)
    if not (hasattr(left_val, 'treatment_duration') and \
            hasattr(mid_val, 'treatment_duration') and \
            hasattr(right_val, 'treatment_duration')):
        raise TypeError("Cannot use median-of-three on list with non-PatientRecord items.")

    # Determine which duration is the median
    # Case 1: Middle is median
    if (left_val.treatment_duration <= mid_val.treatment_duration <= right_val.treatment_duration) or \
       (right_val.treatment_duration <= mid_val.treatment_duration <= left_val.treatment_duration):
        pivot_idx = midIdx
    # Case 2: Left is median
    elif (mid_val.treatment_duration <= left_val.treatment_duration <= right_val.treatment_duration) or \
         (right_val.treatment_duration <= left_val.treatment_duration <= mid_val.treatment_duration):
        pivot_idx = leftIdx
    # Case 3: Right must be median
    else:
        pivot_idx = rightIdx
        
    return pivot_idx

def _random_pivot(leftIdx, rightIdx):
    """
    Helper for Quick Sort: Selects a random pivot index within the range [leftIdx, rightIdx].
    """
    # Ensure range is valid before generating random number
    if leftIdx <= rightIdx:
        try:
             return random.randint(leftIdx, rightIdx)
        except ValueError: # Handle potential errors if indices are invalid
             return leftIdx # Fallback
    else:
        # If leftIdx > rightIdx, the sublist has 0 or 1 element, just return leftIdx
        return leftIdx 

def _doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    """
    Helper for Quick Sort. Partitions the sub-list A[leftIdx...rightIdx]
    around the pivot element (initially at pivotIdx). Modifies the list IN-PLACE.
    Comparison uses 'treatment_duration'. Returns the final index of the pivot.
    """
    # Ensure indices are valid
    if not (0 <= leftIdx < len(A) and 0 <= rightIdx < len(A) and 0 <= pivotIdx < len(A)):
        raise IndexError("Invalid indices provided to partitioning function.")

    pivotVal = A[pivotIdx] # Get the actual PatientRecord object to pivot around
    
    # 1. Move the chosen pivot element to the far right end temporarily
    A[pivotIdx], A[rightIdx] = A[rightIdx], A[pivotIdx]
    
    # 2. Initialize the partition boundary index (currIdx)
    #    Elements to the left of currIdx will be less than the pivot.
    currIdx = leftIdx 
    
    # 3. Iterate through the sub-list (from leftIdx up to rightIdx - 1)
    ii = leftIdx      # The scanner index
    while ii < rightIdx: 
        # Ensure element is a valid PatientRecord (optional safety)
        if not hasattr(A[ii], 'treatment_duration'):
             raise TypeError("Partitioning failed: List contains non-PatientRecord items.")
        
        # Compare current element's duration with the pivot's duration
        if A[ii].treatment_duration < pivotVal.treatment_duration:
            # If smaller than pivot, swap it with the element at the partition boundary
            A[ii], A[currIdx] = A[currIdx], A[ii]
            # Move the partition boundary one position to the right
            currIdx += 1 
        ii += 1 # Move scanner to the next element
        
    # 4. Place the pivot (currently at rightIdx) into its final sorted position
    #    The final position is where the "less than" partition ends (currIdx).
    newPivotIdx = currIdx 
    A[newPivotIdx], A[rightIdx] = A[rightIdx], A[newPivotIdx] # Swap pivot into place
    
    return newPivotIdx # Return the index where the pivot ended up

def _quickSortRecurse(patient_list, left_idx, right_idx, pivot_mode):
    """
    Recursive core function for Quick Sort. Selects pivot, partitions,
    and makes recursive calls on the sub-lists. Sorts IN-PLACE.
    """
    # Base case: If the sub-list has 1 or 0 elements, it's already sorted.
    if right_idx > left_idx:
        
        # --- 1. Pivot Selection ---
        if pivot_mode == 'left':
            pivot_idx = left_idx 
        elif pivot_mode == 'random':
            pivot_idx = _random_pivot(left_idx, right_idx)
        elif pivot_mode == 'median3': # Default to median3 if not specified or invalid
            pivot_idx = _median_of_three(patient_list, left_idx, right_idx)
        else:
             print(f"Warning: Invalid pivot_mode '{pivot_mode}'. Defaulting to 'median3'.")
             pivot_idx = _median_of_three(patient_list, left_idx, right_idx)

        # Ensure selected pivot index is valid before partitioning
        if not (left_idx <= pivot_idx <= right_idx):
             # Handle error: Pivot index is outside the current sub-array bounds
             # This might indicate an issue in pivot selection logic
             # Fallback: Use left index as pivot for safety
             print(f"Warning: Invalid pivot index {pivot_idx} generated. Using left index {left_idx} as fallback.")
             pivot_idx = left_idx

        # --- 2. Partitioning ---
        # Rearrange the list around the pivot and get the pivot's final index
        new_pivot_idx = _doPartitioning(patient_list, left_idx, right_idx, pivot_idx)
        
        # --- 3. Recursive Calls ---
        # Recursively sort the part to the left of the pivot
        _quickSortRecurse(patient_list, left_idx, new_pivot_idx - 1, pivot_mode)
        # Recursively sort the part to the right of the pivot
        _quickSortRecurse(patient_list, new_pivot_idx + 1, right_idx, pivot_mode)
   


def quickSort(patient_list, pivot_mode='median3'):
    """
    Initiates Quick Sort on a list of PatientRecord objects.
    Sorts the list IN-PLACE based on 'treatment_duration' in ascending order.
    Handles potential RecursionError.
    """
    n = len(patient_list)
    # Only sort if list has more than 1 element
    if n > 1:
        try:
            # Start the recursive sorting process
            _quickSortRecurse(patient_list, 0, n - 1, pivot_mode)
        except RecursionError as e: # Catch the specific error
            # Provide informative message
            print(f"\nERROR: Maximum recursion depth exceeded during Quick Sort (pivot='{pivot_mode}').")
            print("This commonly occurs with 'left' pivot on already sorted or reverse-sorted large datasets.")
            
            # Re-raise the error to allow the calling code (like the timer) to handle it
            raise e
        except Exception as e: # Catch other potential errors during sorting
             print(f"\nAn unexpected error occurred during Quick Sort: {e}")
             # Optionally re-raise or handle differently
             raise e 
    