import pytest

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


def test_task_rejects_non_positive_duration():
    with pytest.raises(ValueError, match="greater than zero"):
        Task("Morning walk", 0, "daily", "high")


def test_task_rejects_unknown_priority():
    with pytest.raises(ValueError, match="priority"):
        Task("Morning walk", 20, "daily", "urgent")
