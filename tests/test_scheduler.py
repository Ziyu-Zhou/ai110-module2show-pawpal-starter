import pytest

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
