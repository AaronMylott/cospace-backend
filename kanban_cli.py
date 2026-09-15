#!/usr/bin/env python3

class Task:
    def __init__(self, title, description, status="To Do"):
        self.title = title
        self.description = description
        self.status = status

    def __str__(self):
        return f"{self.title} - {self.description}"


class KanbanBoard:
    STATUSES = ["To Do", "In Progress", "Done"]

    def __init__(self):
        self.tasks = []

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        print("Task added successfully.")

    def move_task(self, title, new_status):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                if new_status not in self.STATUSES:
                    print("Invalid status.")
                    return

                next_status = {
                    "To Do": "In Progress",
                    "In Progress": "Done"
                }
                if next_status.get(task.status) != new_status:
                    print("Invalid move. Tasks can only move forward one state at a time.")
                    return

                task.status = new_status
                print(f"Task moved to '{new_status}'.")
                return
        print("Task not found.")

    def display_board(self):
        print("\n" + "=" * 50)
        print("KANBAN BOARD")
        print("=" * 50)
        for status in self.STATUSES:
            print(f"\n[{status}]")
            print("-" * 30)
            matching_tasks = [t for t in self.tasks if t.status == status]
            if not matching_tasks:
                print("No tasks.")
            else:
                for index, task in enumerate(matching_tasks, start=1):
                    print(f"{index}. {task}")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task.title} ({task.status})")

    def delete_task(self, title):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                self.tasks.remove(task)
                print("Task deleted.")
                return
        print("Task not found.")


def print_menu():
    print("\n=== CLI Kanban Board ===")
    print("1. Add Task")
    print("2. Move Task")
    print("3. Display Board")
    print("4. List Tasks")
    print("5. Delete Task")
    print("6. Exit")


def prompt_for_task_title():
    while True:
        title = input("Task Title: ").strip()
        if title:
            return title
        print("Please enter a task.")


def main():
    board = KanbanBoard()
    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            board.add_task(prompt_for_task_title(), input("Task Description: "))
        elif choice == "2":
            title = input("Task Title: ")
            status = {"1":"To Do","2":"In Progress","3":"Done"}.get(input("1.To Do 2.In Progress 3.Done: "))
            if status:
                board.move_task(title, status)
        elif choice == "3":
            board.display_board()
        elif choice == "4":
            board.list_tasks()
        elif choice == "5":
            board.delete_task(input("Task Title to delete: "))
        elif choice == "6":
            break

if __name__ == "__main__":
    main()
