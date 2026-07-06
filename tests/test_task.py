import pytest
from datetime import date

from pawpal_system import Task


def test_task_stores_its_details():
    task = Task("Morning walk", 20, "daily", "HIGH")

    assert task.description == "Morning walk"
    assert task.duration_minutes == 20
    assert task.frequency == "daily"
    assert task.priority == "high"
    assert task.completed is False


def test_mark_complete_updates_completion_status():
    task = Task("Morning walk", 20, "daily", "high")

    task.mark_complete()

    assert task.completed is True


def test_mark_complete_creates_next_daily_occurrence():
    task = Task(
        "Morning walk",
        20,
        "daily",
        "high",
        due_date=date(2026, 7, 5),
        start_time="08:00",
    )

    next_occurrence = task.mark_complete()

    assert next_occurrence is not task
    assert next_occurrence is not None
    assert next_occurrence.description == task.description
    assert next_occurrence.completed is False
    assert next_occurrence.due_date == date(2026, 7, 6)
    assert next_occurrence.start_time == "08:00"


def test_mark_complete_creates_next_weekly_occurrence():
    task = Task(
        "Brush fur",
        15,
        "weekly",
        "low",
        due_date=date(2026, 7, 5),
    )

    next_occurrence = task.mark_complete()

    assert next_occurrence is not None
    assert next_occurrence.due_date == date(2026, 7, 12)


def test_mark_complete_does_not_recur_once_task():
    task = Task(
        "Vet appointment",
        60,
        "once",
        "high",
        due_date=date(2026, 7, 5),
    )

    assert task.mark_complete() is None
    assert task.completed is True


def test_task_rejects_non_positive_duration():
    with pytest.raises(ValueError, match="greater than zero"):
        Task("Morning walk", 0, "daily", "high")


def test_task_rejects_unknown_priority():
    with pytest.raises(ValueError, match="priority"):
        Task("Morning walk", 20, "daily", "urgent")


def test_task_rejects_invalid_start_time():
    with pytest.raises(ValueError, match="HH:MM"):
        Task(
            "Morning walk",
            20,
            "daily",
            "high",
            start_time="morning",
        )
