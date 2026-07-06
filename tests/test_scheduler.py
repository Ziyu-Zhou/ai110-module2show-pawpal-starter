import pytest
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner_with_tasks(
    *tasks: Task, preferences: str = ""
) -> Owner:
    owner = Owner("Jordan", preferences)
    pet = Pet("Mochi", "dog")
    for task in tasks:
        pet.add_task(task)
    owner.add_pet(pet)
    return owner


def test_scheduler_prioritizes_high_priority_tasks():
    low = Task("Brush fur", 20, "weekly", "low")
    high = Task("Give medicine", 10, "daily", "high")
    owner = make_owner_with_tasks(low, high)
    scheduler = Scheduler(20)

    schedule = scheduler.generate_schedule(owner)

    assert schedule == [high]
    assert scheduler.skipped_tasks == [low]


def test_scheduler_uses_owner_preference_to_break_priority_ties():
    feeding = Task("Evening feeding", 10, "daily", "medium")
    walk = Task("Morning walk", 20, "daily", "medium")
    owner = make_owner_with_tasks(
        feeding, walk, preferences="walk"
    )
    scheduler = Scheduler(20)

    schedule = scheduler.generate_schedule(owner)

    assert schedule == [walk]


def test_scheduler_retrieves_tasks_across_multiple_pets():
    owner = Owner("Jordan", "")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    walk = Task("Morning walk", 20, "daily", "high")
    feeding = Task("Cat breakfast", 10, "daily", "high")
    dog.add_task(walk)
    cat.add_task(feeding)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(30)

    schedule = scheduler.generate_schedule(owner)

    assert schedule == [walk, feeding]


def test_scheduler_skips_completed_tasks():
    completed = Task(
        "Give medicine", 10, "daily", "high", completed=True
    )
    owner = make_owner_with_tasks(completed)
    scheduler = Scheduler(30)

    assert scheduler.generate_schedule(owner) == []
    assert scheduler.skipped_tasks == [completed]
    assert "already complete" in scheduler.explain_schedule()[0]


def test_scheduler_resets_results_before_generating_another_schedule():
    first = Task("Morning walk", 20, "daily", "high")
    second = Task("Brush fur", 10, "weekly", "low")
    scheduler = Scheduler(30)

    scheduler.generate_schedule(make_owner_with_tasks(first))
    schedule = scheduler.generate_schedule(
        make_owner_with_tasks(second)
    )

    assert schedule == [second]
    assert scheduler.scheduled_tasks == [second]
    assert len(scheduler.explain_schedule()) == 1


def test_scheduler_rejects_negative_available_time():
    with pytest.raises(ValueError, match="cannot be negative"):
        Scheduler(-1)


def test_scheduler_sorts_tasks_from_shortest_to_longest():
    long_task = Task("Long walk", 30, "daily", "high")
    short_task = Task("Refill water", 5, "daily", "high")
    medium_task = Task("Brush fur", 15, "weekly", "low")
    tasks = [long_task, short_task, medium_task]

    sorted_tasks = Scheduler(60).sort_by_time(tasks)

    assert sorted_tasks == [short_task, medium_task, long_task]
    assert tasks == [long_task, short_task, medium_task]


def test_scheduler_sorts_tasks_from_longest_to_shortest():
    short_task = Task("Refill water", 5, "daily", "high")
    long_task = Task("Long walk", 30, "daily", "high")

    sorted_tasks = Scheduler(60).sort_by_time(
        [short_task, long_task],
        shortest_first=False,
    )

    assert sorted_tasks == [long_task, short_task]


def test_scheduler_filters_tasks_by_completion_status():
    incomplete = Task("Morning walk", 20, "daily", "high")
    complete = Task(
        "Refill water",
        5,
        "daily",
        "high",
        completed=True,
    )
    owner = make_owner_with_tasks(incomplete, complete)

    tasks = Scheduler(30).filter_tasks(owner, completed=True)

    assert tasks == [complete]


def test_scheduler_filters_tasks_by_pet_name():
    owner = Owner("Jordan", "")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    walk = Task("Morning walk", 20, "daily", "high")
    feeding = Task("Cat breakfast", 10, "daily", "high")
    dog.add_task(walk)
    cat.add_task(feeding)
    owner.add_pet(dog)
    owner.add_pet(cat)

    tasks = Scheduler(30).filter_tasks(owner, pet_name=" luna ")

    assert tasks == [feeding]


def test_scheduler_combines_completion_and_pet_filters():
    owner = Owner("Jordan", "")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    completed_walk = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        completed=True,
    )
    incomplete_feeding = Task("Cat breakfast", 10, "daily", "high")
    dog.add_task(completed_walk)
    cat.add_task(incomplete_feeding)
    owner.add_pet(dog)
    owner.add_pet(cat)

    tasks = Scheduler(30).filter_tasks(
        owner,
        completed=False,
        pet_name="LUNA",
    )

    assert tasks == [incomplete_feeding]


def test_scheduler_adds_next_recurring_task_to_pet():
    pet = Pet("Mochi", "dog")
    task = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        due_date=date(2026, 7, 5),
    )
    pet.add_task(task)

    next_occurrence = Scheduler(30).complete_task(pet, task)

    assert task.completed is True
    assert next_occurrence is not None
    assert next_occurrence.due_date == date(2026, 7, 6)
    assert pet.tasks == [task, next_occurrence]


def test_scheduler_does_not_duplicate_a_completed_recurrence():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 20, "daily", "high")
    pet.add_task(task)
    scheduler = Scheduler(30)

    first_occurrence = scheduler.complete_task(pet, task)
    second_occurrence = scheduler.complete_task(pet, task)

    assert first_occurrence is not None
    assert second_occurrence is None
    assert pet.tasks == [task, first_occurrence]


def test_scheduler_warns_about_cross_pet_time_conflict():
    owner = Owner("Jordan", "")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    walk = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        start_time="08:00",
    )
    feeding = Task(
        "Cat breakfast",
        10,
        "daily",
        "high",
        start_time="08:00",
    )
    dog.add_task(walk)
    cat.add_task(feeding)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(30)

    scheduler.generate_schedule(owner)

    assert scheduler.scheduled_start_times[walk] == "08:00"
    assert scheduler.scheduled_start_times[feeding] == "08:00"
    assert scheduler.conflict_warnings == [
        "Warning: 'Morning walk' (Mochi) conflicts with "
        "'Cat breakfast' (Luna) from 08:00 to 08:10."
    ]


def test_scheduler_warns_about_same_pet_time_conflict():
    first = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        start_time="08:00",
    )
    second = Task(
        "Give medicine",
        10,
        "daily",
        "high",
        start_time="08:15",
    )
    owner = make_owner_with_tasks(first, second)
    scheduler = Scheduler(30)

    scheduler.generate_schedule(owner)

    assert len(scheduler.conflict_warnings) == 1
    assert "from 08:15 to 08:20" in scheduler.conflict_warnings[0]


def test_scheduler_allows_back_to_back_tasks_without_warning():
    first = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        start_time="08:00",
    )
    second = Task(
        "Give medicine",
        10,
        "daily",
        "high",
        start_time="08:20",
    )
    owner = make_owner_with_tasks(first, second)
    scheduler = Scheduler(30)

    scheduler.generate_schedule(owner)

    assert scheduler.conflict_warnings == []


def test_scheduler_assigns_back_to_back_start_times():
    walk = Task("Morning walk", 30, "daily", "high")
    feeding = Task("Feeding", 10, "daily", "high")
    owner = make_owner_with_tasks(walk, feeding)
    scheduler = Scheduler(40)

    scheduler.generate_schedule(owner)

    assert scheduler.scheduled_start_times == {
        walk: "08:00",
        feeding: "08:30",
    }


def test_scheduler_formats_a_daily_plan_for_one_pet():
    walk = Task("Morning walk", 30, "daily", "high")
    feeding = Task("Feeding", 10, "daily", "high")
    owner = make_owner_with_tasks(walk, feeding)
    scheduler = Scheduler(40, start_time="09:15")
    scheduler.generate_schedule(owner)

    plan = scheduler.format_daily_plan(owner)

    assert plan == (
        "Daily plan for Mochi (Dog):\n"
        "  09:15 — Morning walk (30 min) [priority: high]\n"
        "  09:45 — Feeding (10 min) [priority: high]"
    )


def test_scheduler_rejects_invalid_start_time():
    with pytest.raises(ValueError, match="HH:MM"):
        Scheduler(30, start_time="morning")
