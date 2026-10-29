#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

import numpy as np

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
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    ...

def mergeSortRecurse(A, leftIdx, rightIdx):
    ...

def merge(A, leftIdx, midIdx, rightIdx):
    ...

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...

def quickSortRecurse(A, leftIdx, rightIdx):
    ...

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...


