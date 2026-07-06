from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task("Morning walk", 20, "daily", "high")

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 20, "daily", "high")
    original_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == original_task_count + 1


def test_tasks_are_sorted_from_shortest_to_longest():
    long_task = Task("Long walk", 30, "daily", "high")
    short_task = Task("Refill water", 5, "daily", "low")
    medium_task = Task("Brush fur", 15, "weekly", "medium")

    sorted_tasks = Scheduler(60).sort_by_time(
        [long_task, short_task, medium_task]
    )

    assert sorted_tasks == [short_task, medium_task, long_task]


def test_completing_daily_task_creates_task_for_following_day():
    task = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        due_date=date(2026, 7, 5),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 7, 6)


def test_scheduler_flags_tasks_with_duplicate_start_times():
    owner = Owner("Jordan", "")
    pet = Pet("Mochi", "dog")
    walk = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        start_time="08:00",
    )
    feeding = Task(
        "Breakfast",
        10,
        "daily",
        "high",
        start_time="08:00",
    )
    pet.add_task(walk)
    pet.add_task(feeding)
    owner.add_pet(pet)
    scheduler = Scheduler(30)

    scheduler.generate_schedule(owner)

    assert len(scheduler.conflict_warnings) == 1
    assert "conflicts with" in scheduler.conflict_warnings[0]
    assert "from 08:00 to 08:10" in scheduler.conflict_warnings[0]
