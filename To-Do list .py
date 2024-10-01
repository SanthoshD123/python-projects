def show_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Remove a task")
    print("4. Exit")

def add_task(tasks):
    task = input("Enter a new task: ")
    tasks.append(task)
    print(f'Task "{task}" added!')

def view_tasks(tasks):
    if not tasks:
        print("No tasks in the list.")
    else:
        print("\n--- Current Tasks ---")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

def remove_task(tasks):
    view_tasks(tasks)
    try:
        task_index = int(input("Enter the number of the task to remove: ")) - 1
        if 0 <= task_index < len(tasks):
            removed = tasks.pop(task_index)
            print(f'Task "{removed}" removed!')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def todo_app():
    tasks = []
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

# Run the To-Do List app
todo_app()
