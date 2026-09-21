#!/usr/bin/env python3
"""Interactive board supporting both Kanban task flow and Scrum sprint commands."""
import planner_core as core


def prompt(label):
    return input(f"{label}: ").strip()


def prompt_required(label):
    while True:
        value = prompt(label)
        if value:
            return value
        print("  Value required.")


def choose(label, options):
    listing = "  ".join(f"{index}.{option}" for index, option in enumerate(options, start=1))
    answer = prompt(f"{label} ({listing})")
    if answer.isdigit() and 1 <= int(answer) <= len(options):
        return options[int(answer) - 1]
    print("  Invalid choice.")
    return None


def pick_sprint(state, label="Sprint"):
    """Accept a sprint id, its name, or its number in the printed list."""
    if not state.sprints:
        raise ValueError("No sprints exist yet.")
    print(f"\n  {label}s:")
    for index, sprint in enumerate(state.sprints, start=1):
        print(f"    {index}. [{sprint.id}] {sprint.name} - {sprint.status}")
    answer = prompt_required(f"{label} (number, id or name)")

    if answer.isdigit() and 1 <= int(answer) <= len(state.sprints):
        return state.sprints[int(answer) - 1].id
    for sprint in state.sprints:
        if answer.lower() in (sprint.id.lower(), sprint.name.lower()):
            return sprint.id
    raise ValueError(f"No sprint matches '{answer}'.")


def pick_task(state, task_ids=None, label="Task"):
    """Accept a task id, its title, or its number in the printed list."""
    if task_ids is None:
        candidates = list(state.tasks.values())
    else:
        candidates = [state.tasks[task_id] for task_id in task_ids if task_id in state.tasks]
    if not candidates:
        raise ValueError("No tasks to choose from.")
    print(f"\n  {label}s:")
    for index, task in enumerate(candidates, start=1):
        print(f"    {index}. [{task.id}] {task.title} ({task.status})")
    answer = prompt_required(f"{label} (number, id or title)")

    if answer.isdigit() and 1 <= int(answer) <= len(candidates):
        return candidates[int(answer) - 1].id
    for task in candidates:
        if answer.lower() in (task.id.lower(), task.title.lower()):
            return task.id
    raise ValueError(f"No task matches '{answer}'.")


def show_board(state):
    print("\n" + "=" * 60)
    print("KANBAN BOARD")
    print("=" * 60)
    for status in core.TASK_STATUSES:
        print(f"\n[{status}]")
        print("-" * 40)
        matching = [task for task in state.tasks.values() if task.status == status]
        if not matching:
            print("  No tasks.")
        for task in matching:
            sprint = core.sprint_of_task(state, task.id)
            location = sprint.name if sprint else "Backlog"
            print(f"  {task}  ({location})")


def show_backlog(state):
    print("\nBACKLOG")
    print("-" * 40)
    if not state.backlog_task_ids:
        print("  Empty.")
    for entry in core.backlog_readiness(state):
        task = entry["task"]
        marker = "READY" if not entry["reasons"] else "NOT READY"
        print(f"  [{marker}] {task}")
        for reason in entry["reasons"]:
            print(f"      - {reason}")


def show_sprints(state):
    print("\nSPRINTS")
    print("-" * 40)
    if not state.sprints:
        print("  No sprints yet.")
    for sprint in state.sprints:
        print(f"\n  [{sprint.id}] {sprint.name} - {sprint.status}")
        if not sprint.task_ids:
            print("    (no tasks)")
        for task_id in sprint.task_ids:
            task = state.tasks.get(task_id)
            if task:
                print(f"    - {task.title} ({task.status})")
        for card in state.retrospective_cards:
            if card.sprint_id == sprint.id:
                print(f"    * {card.category}: {card.text}")


def print_menu():
    print("\n" + "=" * 60)
    print("  KANBAN + SCRUM PLANNER")
    print("=" * 60)
    print("  Kanban")
    print("    1. Add task to backlog")
    print("    2. Move task forward")
    print("    3. Delete task")
    print("    4. Show board")
    print("    5. Show backlog")
    print("  Scrum")
    print("    6. Create sprint (Planning)")
    print("    7. Start sprint (Active)")
    print("    8. Add task to active sprint")
    print("    9. Complete sprint")
    print("   10. Add retrospective card")
    print("   11. Show sprints")
    print("  Session")
    print("   12. Save")
    print("   13. Reload from disk")
    print("   14. Exit")


def handle(state, choice):
    if choice == "1":
        task = core.create_task(state, prompt_required("Task title"), prompt("Description"))
        print(f"  Added {task.id} to the backlog.")
    elif choice == "2":
        status = choose("Move to", core.TASK_STATUSES)
        if status:
            task = core.move_task(state, pick_task(state), status)
            print(f"  {task.title} is now {task.status}.")
    elif choice == "3":
        task = core.delete_task(state, pick_task(state))
        print(f"  Deleted {task.title}.")
    elif choice == "4":
        show_board(state)
    elif choice == "5":
        show_backlog(state)
    elif choice == "6":
        sprint = core.create_sprint(state, prompt_required("Sprint name"))
        print(f"  Created '{sprint.name}' (id: {sprint.id}) in Planning.")
    elif choice == "7":
        sprint = core.start_sprint(state, pick_sprint(state, "Sprint to start"))
        print(f"  {sprint.name} is now Active.")
    elif choice == "8":
        active = next((s for s in state.sprints if s.status == "Active"), None)
        if active is None:
            print("  No Active sprint. Start one first.")
        else:
            task_id = pick_task(state, state.backlog_task_ids, "Backlog task")
            core.add_task_to_sprint(state, active.id, task_id)
            print(f"  Added to {active.name}.")
    elif choice == "9":
        result = core.complete_sprint(state, pick_sprint(state, "Sprint to complete"))
        print(f"  {result['sprint'].name} is now Completed.")
        print(f"  Delivered {len(result['delivered'])} task(s), {result['velocity']} points.")
        for entry in result["carried_over"]:
            print(f"  Carried over to backlog: {entry['task'].title}")
            for reason in entry["reasons"]:
                print(f"      - {reason}")
    elif choice == "10":
        category = choose("Category", core.RETROSPECTIVE_CATEGORIES)
        if category:
            sprint_id = pick_sprint(state, "Completed sprint")
            card = core.add_retrospective_card(
                state, sprint_id, category, prompt_required("Card text")
            )
            print(f"  Added {card.id}.")
    elif choice == "11":
        show_sprints(state)
    else:
        print("  Unknown option.")


def main():
    try:
        state = core.load_state()
        print(f"Loaded {len(state.tasks)} task(s) and {len(state.sprints)} sprint(s).")
    except (OSError, ValueError) as error:
        print(f"Could not load state: {error}")
        print("Starting empty. Saving will overwrite the existing file.")
        state = core.PlannerState()

    while True:
        print_menu()
        choice = prompt("\nSelect an option")

        if choice == "14":
            break
        if choice == "12":
            try:
                core.save_state(state)
                print(f"  Saved to {core.STATE_FILE}")
            except (OSError, ValueError) as error:
                print(f"  Save failed: {error}")
            continue
        if choice == "13":
            try:
                state = core.load_state()
                print("  Reloaded.")
            except (OSError, ValueError) as error:
                print(f"  Reload failed: {error}")
            continue

        try:
            handle(state, choice)
        except ValueError as error:
            print(f"  Rejected: {error}")


if __name__ == "__main__":
    main()
