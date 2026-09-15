from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

STATE_FILE = Path(__file__).resolve().with_name("state.json")
SPRINT_STATUSES = ["Planning", "Active", "Completed"]
RETROSPECTIVE_CATEGORIES = ["Went Well", "To Improve", "Action Item"]
TASK_STATUSES = ["To Do", "In Progress", "Done"]
IN_PROGRESS_LIMIT = 2

# Fibonacci scale; None means "not yet estimated".
STORY_POINT_VALUES = [1, 2, 3, 5, 8, 13]


def _clean_story_points(value: Any) -> Any:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("story_points must be a number, not a boolean.")
    try:
        points = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"story_points must be a whole number, got {value!r}.")
    if points not in STORY_POINT_VALUES:
        raise ValueError(f"story_points must be one of {STORY_POINT_VALUES}, got {points}.")
    return points


@dataclass
class Sprint:
    name: str
    status: str = "Planning"
    task_ids: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Sprint name cannot be empty.")
        if self.status not in SPRINT_STATUSES:
            raise ValueError(f"Invalid sprint status: {self.status}")
        self.name = self.name.strip()
        self.task_ids = [str(task_id).strip() for task_id in self.task_ids if str(task_id).strip()]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "task_ids": self.task_ids,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Sprint":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            status=data.get("status", "Planning"),
            task_ids=data.get("task_ids", []),
        )


@dataclass
class RetrospectiveCard:
    sprint_id: str
    category: str
    text: str
    id: str = ""

    def __post_init__(self) -> None:
        if not self.sprint_id or not self.sprint_id.strip():
            raise ValueError("Retrospective card must belong to a sprint.")
        if self.category not in RETROSPECTIVE_CATEGORIES:
            raise ValueError(f"Invalid retrospective category: {self.category}")
        if not self.text or not self.text.strip():
            raise ValueError("Retrospective text cannot be empty.")
        self.sprint_id = self.sprint_id.strip()
        self.text = self.text.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sprint_id": self.sprint_id,
            "category": self.category,
            "text": self.text,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RetrospectiveCard":
        return cls(
            id=data.get("id", ""),
            sprint_id=data.get("sprint_id", ""),
            category=data.get("category", "Went Well"),
            text=data.get("text", ""),
        )


@dataclass
class Task:
    title: str
    description: str = ""
    status: str = "To Do"
    id: str = ""
    story_points: Any = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty.")
        if self.status not in TASK_STATUSES:
            raise ValueError(f"Invalid task status: {self.status}")
        self.title = self.title.strip()
        self.description = (self.description or "").strip()
        self.story_points = _clean_story_points(self.story_points)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "story_points": self.story_points,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "To Do"),
            story_points=data.get("story_points"),
        )

    def __str__(self) -> str:
        suffix = f" - {self.description}" if self.description else ""
        points = f" ({self.story_points}pt)" if self.story_points is not None else ""
        return f"[{self.id}] {self.title}{points}{suffix}"


@dataclass
class PlannerState:
    sprints: List[Sprint] = field(default_factory=list)
    retrospective_cards: List[RetrospectiveCard] = field(default_factory=list)
    backlog_task_ids: List[str] = field(default_factory=list)
    tasks: Dict[str, Task] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sprints": [sprint.to_dict() for sprint in self.sprints],
            "retrospective_cards": [card.to_dict() for card in self.retrospective_cards],
            "backlog_task_ids": list(dict.fromkeys(self.backlog_task_ids)),
            "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlannerState":
        tasks_data = data.get("tasks", {})
        if not isinstance(tasks_data, dict):
            tasks_data = {}

        tasks: Dict[str, Task] = {}
        for task_id, payload in tasks_data.items():
            task_id = str(task_id).strip()
            if not task_id:
                continue
            if isinstance(payload, dict):
                task = Task.from_dict({**payload, "id": task_id})
            else:
                # Legacy format stored only the status string.
                task = Task(id=task_id, title=task_id, status=str(payload).strip())
            tasks[task_id] = task

        state = cls(
            sprints=[Sprint.from_dict(item) for item in data.get("sprints", [])],
            retrospective_cards=[RetrospectiveCard.from_dict(item) for item in data.get("retrospective_cards", [])],
            backlog_task_ids=[str(item).strip() for item in data.get("backlog_task_ids", []) if str(item).strip()],
            tasks=tasks,
        )

        for sprint in state.sprints:
            for task_id in sprint.task_ids:
                if task_id not in state.tasks:
                    state.tasks[task_id] = Task(id=task_id, title=task_id)

        return state


def _unique(values: List[str]) -> List[str]:
    return list(dict.fromkeys(values))


def validate_state(state: PlannerState) -> None:
    """Enforce the rules that individual operations cannot check in isolation."""
    sprint_ids = [sprint.id for sprint in state.sprints]
    if len(set(sprint_ids)) != len(sprint_ids):
        raise ValueError("Duplicate sprint ids found in state.")
    if any(not sprint_id for sprint_id in sprint_ids):
        raise ValueError("Every sprint must have a non-empty id.")

    names = [sprint.name.lower() for sprint in state.sprints]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate sprint names found in state.")

    active = [sprint.id for sprint in state.sprints if sprint.status == "Active"]
    if len(active) > 1:
        raise ValueError(f"Only one sprint may be Active, found: {active}")

    card_ids = [card.id for card in state.retrospective_cards]
    if len(set(card_ids)) != len(card_ids):
        raise ValueError("Duplicate retrospective card ids found in state.")

    for task_id, task in state.tasks.items():
        if task.status not in TASK_STATUSES:
            raise ValueError(f"Task '{task_id}' has invalid status '{task.status}'.")

    assigned: Dict[str, str] = {}
    for sprint in state.sprints:
        for task_id in sprint.task_ids:
            if task_id not in state.tasks:
                raise ValueError(f"Sprint '{sprint.id}' references unknown task '{task_id}'.")
            if task_id in assigned:
                raise ValueError(
                    f"Task '{task_id}' is assigned to both '{assigned[task_id]}' and '{sprint.id}'."
                )
            assigned[task_id] = sprint.id
            if task_id in state.backlog_task_ids:
                raise ValueError(
                    f"Task '{task_id}' is in the backlog and assigned to sprint '{sprint.id}'."
                )
            if sprint.status == "Completed" and state.tasks[task_id].status != "Done":
                raise ValueError(
                    f"Completed sprint '{sprint.id}' still holds unfinished task '{task_id}'."
                )

    for task_id in state.backlog_task_ids:
        if task_id not in state.tasks:
            raise ValueError(f"Backlog references unknown task '{task_id}'.")

    sprints_by_id = {sprint.id: sprint for sprint in state.sprints}
    for card in state.retrospective_cards:
        sprint = sprints_by_id.get(card.sprint_id)
        if sprint is None:
            raise ValueError(f"Card '{card.id}' references unknown sprint '{card.sprint_id}'.")
        if sprint.status != "Completed":
            raise ValueError(
                f"Card '{card.id}' belongs to sprint '{sprint.id}' which is {sprint.status}, not Completed."
            )
        if card.category not in RETROSPECTIVE_CATEGORIES:
            raise ValueError(f"Card '{card.id}' has invalid category '{card.category}'.")


def load_state(file_path: Path = STATE_FILE) -> PlannerState:
    if not file_path.exists():
        empty_state = PlannerState()
        save_state(empty_state, file_path)
        return empty_state

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("State file must contain a JSON object.")

    state = PlannerState.from_dict(data)
    validate_state(state)
    return state


def save_state(state: PlannerState, file_path: Path = STATE_FILE) -> None:
    validate_state(state)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(state.to_dict(), file, indent=2)
        file.write("\n")


def find_sprint(state: PlannerState, sprint_id: str) -> Sprint:
    for sprint in state.sprints:
        if sprint.id == sprint_id:
            return sprint
    raise ValueError(f"Sprint with id '{sprint_id}' was not found.")


def _next_id(prefix: str, existing_ids: List[str]) -> str:
    taken = set(existing_ids)
    index = 1
    while f"{prefix}-{index}" in taken:
        index += 1
    return f"{prefix}-{index}"


def create_sprint(state: PlannerState, name: str) -> Sprint:
    if not name or not name.strip():
        raise ValueError("Sprint name cannot be empty.")

    name = name.strip()
    if any(sprint.name.lower() == name.lower() for sprint in state.sprints):
        raise ValueError(f"A sprint named '{name}' already exists.")

    sprint_id = _next_id("sprint", [sprint.id for sprint in state.sprints])
    sprint = Sprint(id=sprint_id, name=name, status="Planning", task_ids=[])
    state.sprints.append(sprint)
    return sprint


def start_sprint(state: PlannerState, sprint_id: str) -> Sprint:
    sprint = find_sprint(state, sprint_id)
    if sprint.status != "Planning":
        raise ValueError(f"Sprint '{sprint_id}' cannot be started because it is not in Planning state.")

    active_sprint = next((item for item in state.sprints if item.status == "Active" and item.id != sprint.id), None)
    if active_sprint is not None:
        raise ValueError(f"Cannot start sprint '{sprint_id}' because sprint '{active_sprint.id}' is already Active.")

    sprint.status = "Active"
    return sprint


def find_task(state: PlannerState, task_id: str) -> Task:
    task = state.tasks.get(str(task_id).strip())
    if task is None:
        raise ValueError(f"Task with id '{task_id}' was not found.")
    return task


def create_task(state: PlannerState, title: str, description: str = "", story_points: Any = None) -> Task:
    """Create a backlog task. Use add_task_to_sprint to pull it into a sprint."""
    task_id = _next_id("task", list(state.tasks))
    task = Task(id=task_id, title=title, description=description, story_points=story_points)
    state.tasks[task_id] = task
    state.backlog_task_ids.append(task_id)
    return task


def estimate_task(state: PlannerState, task_id: str, story_points: Any) -> Task:
    task = find_task(state, task_id)
    task.story_points = _clean_story_points(story_points)
    return task


def sprint_of_task(state: PlannerState, task_id: str) -> Sprint:
    for sprint in state.sprints:
        if task_id in sprint.task_ids:
            return sprint
    return None


def move_task(state: PlannerState, task_id: str, new_status: str) -> Task:
    task = find_task(state, task_id)
    if new_status not in TASK_STATUSES:
        raise ValueError(f"Invalid task status: {new_status}")

    forward = {"To Do": "In Progress", "In Progress": "Done"}
    if forward.get(task.status) != new_status:
        raise ValueError(
            f"Task '{task_id}' cannot move from '{task.status}' to '{new_status}'. "
            "Tasks move forward one column at a time."
        )

    if new_status == "In Progress":
        in_progress = sum(1 for item in state.tasks.values() if item.status == "In Progress")
        if in_progress >= IN_PROGRESS_LIMIT:
            raise ValueError(
                f"WIP limit reached. Only {IN_PROGRESS_LIMIT} tasks may be In Progress at once."
            )

    task.status = new_status
    return task


def delete_task(state: PlannerState, task_id: str) -> Task:
    task = find_task(state, task_id)
    del state.tasks[task.id]
    state.backlog_task_ids = [item for item in state.backlog_task_ids if item != task.id]
    for sprint in state.sprints:
        if task.id in sprint.task_ids:
            sprint.task_ids.remove(task.id)
    return task


def add_task_to_sprint(state: PlannerState, sprint_id: str, task_id: str) -> Sprint:
    sprint = find_sprint(state, sprint_id)
    if sprint.status != "Active":
        raise ValueError(f"Tasks can only be added to an Active sprint. Current status: {sprint.status}")

    task = find_task(state, task_id)
    owner = sprint_of_task(state, task.id)
    if owner is not None and owner.id != sprint.id:
        raise ValueError(f"Task '{task.id}' is already assigned to sprint '{owner.id}'.")

    if task.id in state.backlog_task_ids:
        state.backlog_task_ids = [item for item in state.backlog_task_ids if item != task.id]
    if task.id not in sprint.task_ids:
        sprint.task_ids.append(task.id)

    return sprint


def complete_sprint(state: PlannerState, sprint_id: str) -> Sprint:
    sprint = find_sprint(state, sprint_id)
    if sprint.status != "Active":
        raise ValueError(f"Sprint '{sprint_id}' cannot be completed because it is not Active.")

    remaining_task_ids: List[str] = []
    for task_id in sprint.task_ids:
        task = state.tasks.get(task_id)
        if task is not None and task.status == "Done":
            remaining_task_ids.append(task_id)
        else:
            if task is not None:
                task.status = "To Do"
            if task_id not in state.backlog_task_ids:
                state.backlog_task_ids.append(task_id)

    sprint.task_ids = remaining_task_ids
    sprint.status = "Completed"
    state.backlog_task_ids = _unique(state.backlog_task_ids)
    return sprint


def add_retrospective_card(state: PlannerState, sprint_id: str, category: str, text: str) -> RetrospectiveCard:
    sprint = find_sprint(state, sprint_id)
    if sprint.status != "Completed":
        raise ValueError("Retrospective cards can only be added to a Completed sprint.")

    category = category.strip()
    text = text.strip()
    if category not in RETROSPECTIVE_CATEGORIES:
        raise ValueError(f"Invalid category. Allowed values: {RETROSPECTIVE_CATEGORIES}")
    if not text:
        raise ValueError("Retrospective text cannot be empty.")

    card = RetrospectiveCard(
        id=_next_id("card", [item.id for item in state.retrospective_cards]),
        sprint_id=sprint_id,
        category=category,
        text=text,
    )
    state.retrospective_cards.append(card)
    return card


def _show(label: str, action) -> None:
    """Run an action and report whether validation allowed or blocked it."""
    try:
        action()
        print(f"  ALLOWED  {label}")
    except ValueError as error:
        print(f"  BLOCKED  {label}\n           -> {error}")


def main() -> None:
    # Demonstration run: starts from an empty board so it is repeatable.
    state = PlannerState()

    print("=" * 70)
    print("1. SPRINT EXCLUSIVITY - only one Active sprint at a time")
    print("=" * 70)
    sprint_one = create_sprint(state, "Sprint 1")
    sprint_two = create_sprint(state, "Sprint 2")
    print(f"  Created {sprint_one.id} and {sprint_two.id}, both in Planning.")
    _show(f"start {sprint_one.id}", lambda: start_sprint(state, sprint_one.id))
    _show(f"start {sprint_two.id} while {sprint_one.id} is Active",
          lambda: start_sprint(state, sprint_two.id))

    print()
    print("=" * 70)
    print("3a. RETROSPECTIVE LOCKDOWN - blocked while the sprint is Active")
    print("=" * 70)
    _show("add card to an Active sprint",
          lambda: add_retrospective_card(state, sprint_one.id, "Went Well", "Too early."))

    print()
    print("=" * 70)
    print("2. UNFINISHED WORK - returned to the backlog on completion")
    print("=" * 70)
    task_a = create_task(state, "Build login form", "Email and password fields")
    task_b = create_task(state, "Wire up signup", "Depends on the login form")
    add_task_to_sprint(state, sprint_one.id, task_a.id)
    add_task_to_sprint(state, sprint_one.id, task_b.id)
    move_task(state, task_a.id, "In Progress")
    move_task(state, task_a.id, "Done")
    move_task(state, task_b.id, "In Progress")
    print(f"  Before: sprint tasks {sprint_one.task_ids}, backlog {state.backlog_task_ids}")
    print(f"          {task_a.id}={task_a.status}, {task_b.id}={task_b.status}")
    complete_sprint(state, sprint_one.id)
    print(f"  After : sprint tasks {sprint_one.task_ids}, backlog {state.backlog_task_ids}")
    print(f"          {task_b.id} was unfinished -> reset to '{task_b.status}' in the backlog")

    print()
    print("=" * 70)
    print("3b. RETROSPECTIVE LOCKDOWN - allowed once the sprint is Completed")
    print("=" * 70)
    _show("add 'Went Well' card to the Completed sprint",
          lambda: add_retrospective_card(
              state, sprint_one.id, "Went Well",
              "The team finished planning early and aligned on scope."))
    _show("add 'To Improve' card to the Completed sprint",
          lambda: add_retrospective_card(
              state, sprint_one.id, "To Improve",
              "We should reduce context switching during implementation."))
    _show("add card with category 'Blocker' to the Completed sprint",
          lambda: add_retrospective_card(state, sprint_one.id, "Blocker", "Not an allowed category."))

    print()
    print("=" * 70)
    print("NEXT SPRINT - the backlog item is available again")
    print("=" * 70)
    start_sprint(state, sprint_two.id)
    print(f"  {sprint_two.id} is now Active (allowed, no other sprint is running).")
    add_task_to_sprint(state, sprint_two.id, task_b.id)
    print(f"  Pulled {task_b.id} from the backlog: sprint tasks {sprint_two.task_ids}, "
          f"backlog {state.backlog_task_ids}")

    save_state(state)
    print(f"\nState saved to {STATE_FILE}")


if __name__ == "__main__":
    main()