def moveDisk(src, dest, n, level):
    print(f"{' ' * level}Recursion level={level}")
    print(f"{' ' * level}Moving disk {n} from Source {src} to Destination {dest}")
    print(f"n={n}, src={src}, dest={dest}")

def towers_of_hanoi_Algorithm(n, src, dest, level=1):
    if (n == 1):
       # This is the base case. The recursion stops when there is only one disk to move.
       moveDisk(src, dest, 1, level) # 1 represents the smallest disk which is at the top
    else:
        tmp = 6 - (src + dest)
        towers_of_hanoi_Algorithm(n - 1, src, tmp, level + 1)  # Recursively move n-1 disks from the source to the temporary peg.
        moveDisk(src, dest, n, level) # Move the nth (largest disk) disk from the source to the destination.
        towers_of_hanoi_Algorithm(n - 1, tmp, dest, level + 1) # Recursively move n-1 disks from the temporary peg to the destination.

def main():
    try:
        n = int(input("Enter the numbers of disk: "))
        if n < 1:
            raise ValueError("Number of disks must be greater than 0.")
        towers_of_hanoi_Algorithm(n, 1, 3)  # We start the recursion with peg 1 as the source and peg 3 as the destination.
    except ValueError as e:
           print(f"Error: {e}")

if __name__ == "__main__":
    main()

 
 



