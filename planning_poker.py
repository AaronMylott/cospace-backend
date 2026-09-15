#!/usr/bin/env python3
"""Planning Poker: three mock developers estimate a task in Fibonacci points."""
import argparse
import random
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional

FIBONACCI = [1, 2, 3, 5, 8, 13]
MAX_ROUNDS = 3


@dataclass
class Developer:
    name: str
    # How far this developer leans from the task's true size, in scale positions.
    bias: int
    style: str

    def vote(self, true_index: int, rng: random.Random) -> int:
        spread = rng.choice([-1, 0, 0, 1])
        index = _clamp(true_index + self.bias + spread)
        return FIBONACCI[index]

    def revote(self, own: int, group_median: float, rng: random.Random) -> int:
        """Move one step toward the group after hearing the discussion."""
        own_index = FIBONACCI.index(own)
        target_index = _nearest_index(group_median)
        if own_index == target_index:
            return own
        step = 1 if target_index > own_index else -1
        stubborn = rng.random() < 0.25
        return FIBONACCI[_clamp(own_index + (0 if stubborn else step))]


TEAM = [
    Developer("Ana", bias=-1, style="optimist, has seen it all before"),
    Developer("Ben", bias=0, style="pragmatist, estimates from the middle"),
    Developer("Cara", bias=1, style="cautious, always prices in the unknowns"),
]


def _clamp(index: int) -> int:
    return max(0, min(len(FIBONACCI) - 1, index))


def _nearest_index(value: float) -> int:
    return min(range(len(FIBONACCI)), key=lambda i: abs(FIBONACCI[i] - value))


def nearest_fibonacci(value: float) -> int:
    return FIBONACCI[_nearest_index(value)]


def is_consensus(votes: Dict[str, int]) -> bool:
    return len(set(votes.values())) == 1


def is_adjacent(votes: Dict[str, int]) -> bool:
    """Votes sit on neighbouring cards, which counts as close enough to settle."""
    indexes = sorted(FIBONACCI.index(vote) for vote in votes.values())
    return indexes[-1] - indexes[0] <= 1


def show_votes(votes: Dict[str, int]) -> None:
    for name, vote in votes.items():
        print(f"    {name:<6} {vote:>3}")
    values = list(votes.values())
    print(f"    {'-' * 12}")
    print(f"    average  {statistics.mean(values):>5.1f}")
    print(f"    median   {statistics.median(values):>5.1f}")
    print(f"    spread   {min(values)} - {max(values)}")


def discuss(votes: Dict[str, int]) -> None:
    low = min(votes, key=votes.get)
    high = max(votes, key=votes.get)
    print(f"\n  Discussion:")
    print(f"    {low} argues for {votes[low]} - smaller than the rest of the team sees it.")
    print(f"    {high} argues for {votes[high]} - flags risk the others have not priced in.")


def run_session(title: str, seed: Optional[int] = None, rounds: int = MAX_ROUNDS) -> int:
    rng = random.Random(seed)
    true_index = rng.randrange(len(FIBONACCI))

    print("=" * 56)
    print(f"PLANNING POKER - {title}")
    print("=" * 56)
    print("Team:")
    for developer in TEAM:
        print(f"  {developer.name:<6} {developer.style}")

    votes = {developer.name: developer.vote(true_index, rng) for developer in TEAM}

    for round_number in range(1, rounds + 1):
        print(f"\nRound {round_number}")
        print("-" * 56)
        show_votes(votes)

        if is_consensus(votes):
            agreed = next(iter(votes.values()))
            print(f"\n  Consensus reached: {agreed} points.")
            return agreed

        if round_number == rounds:
            break

        discuss(votes)
        median = statistics.median(list(votes.values()))
        votes = {
            developer.name: developer.revote(votes[developer.name], median, rng)
            for developer in TEAM
        }

    values = list(votes.values())
    agreed = nearest_fibonacci(statistics.mean(values))
    reason = "votes were adjacent" if is_adjacent(votes) else f"no consensus after {rounds} rounds"
    print(f"\n  {reason.capitalize()}; settling on the nearest card to the average.")
    print(f"  Agreed estimate: {agreed} points.")
    return agreed


def apply_to_task(task_id: str, points: int) -> None:
    import planner_core as core

    state = core.load_state()
    task = core.estimate_task(state, task_id, points)
    core.save_state(state)
    print(f"\n  Saved: '{task.title}' estimated at {task.story_points} points.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", default="Untitled task",
                        help="what the team is estimating")
    parser.add_argument("--task", help="task id in state.json to record the estimate against")
    parser.add_argument("--seed", type=int, help="fix the random seed for a repeatable session")
    parser.add_argument("--rounds", type=int, default=MAX_ROUNDS,
                        help=f"maximum voting rounds (default {MAX_ROUNDS})")
    args = parser.parse_args()

    points = run_session(args.title, seed=args.seed, rounds=args.rounds)

    if args.task:
        try:
            apply_to_task(args.task, points)
        except (OSError, ValueError) as error:
            print(f"\n  Could not record the estimate: {error}")


if __name__ == "__main__":
    main()
