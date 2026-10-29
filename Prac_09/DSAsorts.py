#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

import numpy as np
import random

def bubbleSort(A):
    n = len(A)
    pass_num = 0
    swapped = True

    while swapped and pass_num < n - 1:
        # At the start of a new pass, reset the boolean
        swapped = False 
        # Inner loop for comparing adjacent elements.
        for i in range(n - 1 - pass_num):
          if A[i] > A[i+1]:
            # Swap out-of-order elements.
              temp = A[i]
              A[i] = A[i+1]
              A[i+1] = temp
              swapped = True
    
        pass_num += 1

def insertionSort(A):
    n = len(A)

    # Iterate through the unsorted part of the list.
    for nn in range(1, n-1):
        ii = nn
        # Shuffle the element left into the sorted sublist.
        while ii > 0 and A[ii-1] > A[ii]:
            # Swap the element with the one on its left.
            temp = A[ii]
            A[ii] = A[ii-1]
            A[ii-1] = temp
            # Move left to continue the insertion process.
            ii -= 1
 
    

def selectionSort(A):
    n = len(A)

    # Outer loop defines the sorted boundary.
    for nn in range(n):
        # Find the index of the minimum element.
        min_index = nn
        # Inner loop finds the index of the smallest element in the unsorted part.
        for jj in range(nn + 1, n):
             if A[jj] < A[min_index]:
                 min_index = jj # stores the current min value in the min_index
        # Swap the minimum element into its correct position.         
        temp = A[min_index]
        A[min_index] = A[nn]
        A[nn] = temp


def mergeSort(A):
    """
    Wrapper function to initiate the merge sort process.
    """
    mergeSortRecurse(A, 0, len(A) - 1)

def mergeSortRecurse(A, leftIdx, rightIdx):
    """
    The recursive part of merge sort. It divides the array into halves.
    """
    # Base case: if the subarray has more than one element.
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2 # Find the middle index.
        
        # Recursively sort the left half.
        mergeSortRecurse(A, leftIdx, midIdx)
        
        # Recursively sort the right half.
        mergeSortRecurse(A, midIdx + 1, rightIdx)
        
        # Merge the two sorted halves back together.
        merge(A, leftIdx, midIdx, rightIdx)

def merge(A, leftIdx, midIdx, rightIdx):
    """
    Merges two sorted subarrays back into the original array A.
    """
    # Create temporary arrays for the left and right halves.
    len_L = midIdx - leftIdx + 1 # Calculates the length of the left temporary array.
    len_R = rightIdx - midIdx # Calculates the length of the right temporary array.
    
    temp_L = [0] * len_L # Creates the temporary array for the left half.
    temp_R = [0] * len_R # Creates the temporary array for the right half.

    # Copy data to the temporary arrays.
    for i in range(len_L):
        temp_L[i] = A[leftIdx + i]
    for j in range(len_R):
        temp_R[j] = A[midIdx + 1 + j]
        
    # Merge the temporary arrays back into the main array A.
    i = 0 # Initial index of the left temporary array.
    j = 0 # Initial index of the right temporary array.
    k = leftIdx # Initial index of the merged array.

    while i < len_L and j < len_R: # Loop that compares and merges elements from both temporary arrays.
        if temp_L[i] <= temp_R[j]: # Compares the elements at the front of each temporary array.
            A[k] = temp_L[i] # If the left element is smaller, places it in the main array.
            i += 1 # Moves the pointer for the left temporary array forward.
        else: # If the right element is smaller.
            A[k] = temp_R[j] # Places the right element in the main array.
            j += 1 # Moves the pointer for the right temporary array forward.
        k += 1 # Moves the pointer for the main array forward.

    # Copy any remaining elements from the left temporary array.
    while i < len_L:
        A[k] = temp_L[i]
        i += 1
        k += 1
        
    # Copy any remaining elements from the right temporary array.
    while j < len_R:
        A[k] = temp_R[j]
        j += 1
        k += 1

def quickSortMedian3(A):
    """
    Wrapper function to initiate the median-of-three quick sort process.
    """
    quickSortRecurse(A, 0, len(A) - 1, "median")

def quickSortRandom(A):
    """
    Wrapper function to initiate the random pivot quick sort process.
    """
    quickSortRecurse(A, 0, len(A) - 1, "random")


def quickSort(A):
    """
    Wrapper function to initiate the quick sort process.
    """
    quickSortRecurse(A, 0, len(A) - 1, "left")
    

def quickSortRecurse(A, leftIdx, rightIdx, pivot_mode):
   """
    The single, flexible recursive function for all quick sort versions.
    """
    # Base case: if the subarray has more than one element.
   if rightIdx > leftIdx:
        
        # pivot selection logic
        if pivot_mode == "left": # Checks if the strategy is to use the left-most pivot.
            pivotIdx = leftIdx # Selects the first element of the subarray as the pivot

        elif pivot_mode == "median": # Checks if the strategy is median-of-three.
            midIdx = (leftIdx + rightIdx) // 2 # Finds the middle index.
            # Sort the left, middle, and right elements to find the median
            if A[leftIdx] > A[midIdx]: A[leftIdx], A[midIdx] = A[midIdx], A[leftIdx]
            if A[leftIdx] > A[rightIdx]: A[leftIdx], A[rightIdx] = A[rightIdx], A[leftIdx]
            if A[midIdx] > A[rightIdx]: A[midIdx], A[rightIdx] = A[rightIdx], A[midIdx]
            pivotIdx = midIdx # The middle index now holds the median, which is chosen as the pivot.
        
        elif pivot_mode == "random": # Checks if the strategy is to use a random pivot.
            pivotIdx = random.randint(leftIdx, rightIdx) # Selects a random index within the subarray as the pivot.
        
        # Partition the array around the chosen pivot
        newPivotIdx = doPartitioning(A, leftIdx, rightIdx, pivotIdx) # Calls the partitioning function to rearrange the array.
        
        # Recursively sort the left and right partitions
        quickSortRecurse(A, leftIdx, newPivotIdx - 1, pivot_mode) # Recursively sorts the partition to the left of the pivot.
        quickSortRecurse(A, newPivotIdx + 1, rightIdx, pivot_mode) # Recursively sorts the partition to the right of the pivot.

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    """
    Partitions the array around a pivot value.
    """
    pivotVal = A[pivotIdx] # Stores the value of the chosen pivot.
    
    # Swaps the pivot to the far right to get it out of the way.
    A[pivotIdx], A[rightIdx] = A[rightIdx], A[pivotIdx]
    
    currIdx = leftIdx # Initializes a pointer for the boundary of the "less than pivot" section.
    
    # Iterate through the array to partition elements.
    ii = leftIdx
    while ii < rightIdx:
        # If an element is smaller than the pivot, move it to the left partition.
        if A[ii] < pivotVal:
            A[ii], A[currIdx] = A[currIdx], A[ii]
            currIdx += 1 # Move the partition boundary.
        ii += 1 # Moves the scanner to the next element.
        
    # The final position for the pivot is where the "less than" section ends.
    newPivotIdx = currIdx 
    
    # Swaps the pivot from the far right into its final sorted position.
    A[rightIdx], A[newPivotIdx] = A[newPivotIdx], pivotVal
    
    return newPivotIdx


