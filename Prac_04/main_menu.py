from Linked_List import DSALinkedList

# Create one instance of the list that the menu will operate on
my_list = DSALinkedList()
running = True

while running:
    print("\n--- Linked List Menu ---")
    print("1. Insert First")
    print("2. Insert Last")
    print("3. Remove First")
    print("4. Remove Last")
    print("5. Display the list")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        value = input("Enter the value to insert at the front: ")
        my_list.insertFirst(value)
        print(f"'{value}' has been inserted.")

    elif choice == '2':
        value = input("Enter the value to insert at the end: ")
        my_list.insertLast(value)
        print(f"'{value}' has been inserted.")

    elif choice == '3':
        try:
            removed_value = my_list.removeFirst()
            print(f"Removed '{removed_value}' from the front of the list.")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '4':
        try:
            removed_value = my_list.removeLast()
            print(f"Removed '{removed_value}' from the end of the list.")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '5':
        my_list.display()

    elif choice == '6':
        running = False
        print("Exiting program.")
        
    else:
        print("Invalid choice, please try again.")