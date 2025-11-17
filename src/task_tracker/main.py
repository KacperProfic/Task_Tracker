import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder, w którym jest skrypt
FILE_PATH = os.path.join(BASE_DIR, "task.json")


def exit_program():
    print("Exiting the program. Goodbye!")
    exit()


def add_task(tasks):
    description = input("Enter a task description:\n>>").strip()
    if not description:
        print("Description cannot be empty")
        return
    new_id = generate_id(tasks)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(new_task)
    print(f"Added new task with id {new_id}")


def generate_id(tasks):
    if not tasks:
        return 1
    max_size = 0
    for task in tasks:
        if isinstance(task["id"], int):
            max_size = max(max_size, task["id"])
    return max_size + 1


def update_task(tasks):
    try:
        update_id = int(input("Enter ID: ").strip())
    except ValueError:
        print("ID musi być liczbą!")
        return

    task_to_update = None
    for task in tasks:
        if task["id"] == update_id:
            task_to_update = task
            break

    if task_to_update is None:
        print(f"Task with ID {update_id} not found.")
        return

    changed = False

    print("Co chcesz zmienić? (description/status)")
    choice = input().strip().lower()

    if choice == "description":
        new_desc = input("Nowy opis (Enter = bez zmian): ").strip()
        if new_desc:
            task_to_update["description"] = new_desc
            changed = True

    elif choice == "status":
        new_status = input("Nowy status (todo/in progress/done): ").strip()
        if not new_status:
            print("Status nie może być pusty!")
            return
        if new_status not in ("todo", "in progress", "done"):
            print("Niepoprawny status!")
            return
        task_to_update["status"] = new_status
        changed = True

    else:
        print("Wybierz description lub status!")
        return

    if changed:
        task_to_update["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Zadanie zaktualizowane!")


def delete_task(tasks):
    try:
        delete_id = int(input("Enter ID: ").strip())
    except ValueError:
        print("Must be an integer!")
        return

    index = -1
    for i, task in enumerate(tasks):
        if task["id"] == delete_id:
            index = i
            break
    if index == -1:
        print(f"Task with ID {delete_id} not found!")
        return
    removed_task = tasks.pop(index)
    print(f"Usunięto: {removed_task['description']}")


def list_all_tasks(tasks):
    for task in tasks:
        print(
            f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}"
        )


def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    if os.path.getsize(FILE_PATH) == 0:
        return []
    with open(FILE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_task(tasks):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def main():
    tasks = load_tasks()

    while True:
        print("**WELCOME HERE IS YOUR TASK TRACKER!**\n")
        print("Commands List: Add, Update, Delete, ListAll, Exit")
        user_input = input("What do you want to do?\n>>")

        if user_input.lower() == "exit":
            exit_program()
            break
        elif user_input.lower() == "add":
            add_task(tasks)
            save_task(tasks)

        elif user_input.lower() == "update":
            update_task(tasks)
            save_task(tasks)
        elif user_input.lower() == "delete":
            delete_task(tasks)
            save_task(tasks)
        elif user_input.lower() == "listall":
            list_all_tasks(tasks)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
