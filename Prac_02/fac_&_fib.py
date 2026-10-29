
import time

# Itertaive factorial (loop based)
def calc_factorial_Iteraive(n):
    nfactorial = 1
    for ii in range(n, 1, -1): # This loop iterates backward from n down to 2
        nfactorial = nfactorial * ii
    return nfactorial

# Recursive factorial ( where the function calls itself)
def calc_factorial_Recursive(n):
    # This is the base case. The recursion stops when n is 0 
    if (n == 0):
        return 1
    # This is the recursive step. The function calls itself with a smaller number (n-1)
    else:
        return n * calc_factorial_Recursive(n-1)

# Iterative fibonacci (This method is highly efficient because it never has to recalculate a number it has already found.)
def fib_Iterative(n):
    # This function calculates the n-th Fibonacci number using an iterative approach.
    # It's more efficient than the recursive version for large numbers.
    fibVal = 0
    currVal = 1
    lastVal = 0

    if (n == 0):
        fibVal = 0
    elif (n == 1):
        fibVal = 1
    else:
       # The loop starts from 2 and continues up to n.
       for ii in range(2, n+1):
            fibVal = currVal + lastVal  # The next Fibonacci number is the sum of the last two.
            # We update the values to prepare for the next iteration.
            lastVal = currVal
            currVal = fibVal
    return fibVal
    
# Recursive fibonacci
def fib_Recursive(n):
    # This function calculates the n-th Fibonacci number using recursion.
    # These are the base cases for the recursion.
    if (n == 0):
        fibVal = 0
    elif (n == 1):
        fibVal = 1
    else:
        # This is the recursive step, which adds the two previous Fibonacci numbers.
        fibVal = fib_Recursive(n - 1) + fib_Recursive(n - 2)
    return fibVal

# Source: https://medium.com/rain-coffee-and-contemplation/recursion-basics-using-euclids-algorithm-for-computing-gcd-732500fe1c99
def gcd_recursive(a, b):
    # This is the base case. The recursion stops when the second number (b) is 0.
    if b == 0:
        return a
    # This is the recursive step. The function calls itself with b and the remainder of a divided by b.
    else:
        return gcd_recursive(b, a % b) # reversed so it takes first as larger no as reminder of both (a and b) in second will always be lesser
    
# Source: https://www.apcomputersciencetutoring.com/recursive-base-conversion-practice-problem/    
def convert_to_base_recursive(n, base):
    # This string holds the characters for digits in different bases,
    # from 0 to 9 for base 10, and A-F for bases 11-16.
    digits = "0123456789ABCDEF"
    # This is the base case. The recursion stops when the number (n) is 0.
    # It returns an empty string, which is the starting point for building the result.
    if n == 0:
        return ""
    # We recursively call the function with the integer division (n // base)
    # and then add the digit of the remainder (n % base) to the end.
    else:
        return convert_to_base_recursive(n // base, base) + digits[n % base]    


def test_question_1():
    try: # try block handles potential ValueErrors, such as when a user enters text instead of a number
        n = int(input("Enter a non-negative value for n to test Factorial and Fibonacci: "))
        if n < 0:
            raise ValueError("Input must be a non-negative value.")
        print(f"\n--- Testing with n = {n} ---")

        # Test Iterative Factorial
        print(f"\n--- Running Iterative Factorial ---")
        start_time = time.time() # Records the start time to measure performance by calculating runtime
        result_factorial_Iterative = calc_factorial_Iteraive(n)
        end_time = time.time() # Records the end time to measure performance by calculating runtime
        print(f"Result: {result_factorial_Iterative}")
        print(f"Time taken: {end_time - start_time:.6f} seconds") # Calculates and prints the runtime.

        # Test Recursive Factorial
        print(f"\n--- Running Recursive Factorial ---")
        try:  # This nested try block specifically handles a RecursionError, which is unique to recursive functions as they can reach a limit
              # linear recursive depth, for input n, calls itself n times
            start_time = time.time()
            result_factorial_Recursive = calc_factorial_Recursive(n)
            end_time = time.time()
            print(f"Result: {result_factorial_Recursive}")
            print(f"Time taken: {end_time - start_time:.6f} seconds")
        except RecursionError:
            print(f"Error: Recursion limit exceeded for n = {n}")

        # Test Iterative Fibonacci
        print(f"\n--- Running Iterative Fibonacci ---")
        start_time = time.time()
        result_fibonacci_Iterative = fib_Iterative(n)
        end_time = time.time()
        print(f"Result: {result_fibonacci_Iterative}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")

        # Test Recursive Fibonacci
        print(f"\n--- Running Recursive Fibonacci ---")
        start_time = time.time()
        result_fibonacci_recursive = fib_Recursive(n)
        end_time = time.time()
        print(f"Result: {result_fibonacci_recursive}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
       
    # This except block catches the ValueError raised by int()        
    except ValueError as e:
        print(f"Invalid input: {e}")
    # This is a catch-all for any other unexpected errors.    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def test_question_2():
    try:
        print(f"\n--- Testing Greatest Common Denominator (GCD) ---")
        a = int(input("Enter the first positive integer for GCD: "))
        b = int(input("Enter the second positive integer for GCD: "))
        if a < 0 or b < 0:
            raise ValueError("GCD inputs must be non-negative integers.")
        start_time = time.time()
        result = gcd_recursive(a, b)
        end_time = time.time()
        print(f"The GCD of {a} and {b} is: {result}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
    except ValueError as e:
        print(f"Invalid input: {e}")


def test_question_3():
    try:
        print(f"\n--- Testing Recursive Number Conversions ---")
        dec_num = int(input("Enter a decimal number to convert: "))
        new_base = int(input("Enter the new base (2-16): "))
        if dec_num < 0:
            raise ValueError("The number to convert must be non-negative.")
        if new_base < 2 or new_base > 16:
            raise ValueError("The new base must be between 2 and 16.")
        start_time = time.time()
        converted_result = convert_to_base_recursive(dec_num, new_base)
        end_time = time.time()
        if dec_num == 0:
            print(f"The decimal number {dec_num} in base {new_base} is: 0")
        else:
            print(f"The decimal number {dec_num} in base {new_base} is: {converted_result}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
    except ValueError as e:
        print(f"Invalid input: {e}")


def main():
    running = True # a flag variable that controls whether the main loop continues to run
    while running:
        print("\n--- Menu Options ---")
        print("1. Test Question 1 (Factorial and Fibonacci)")
        print("2. Test Question 2 (GCD)")
        print("3. Test Question 3 (Number Conversion)")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            test_question_1()
        elif choice == '2':
            test_question_2()
        elif choice == '3':
            test_question_3()
        elif choice == '4':
            print("Exiting program.")
            running = False
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()

        