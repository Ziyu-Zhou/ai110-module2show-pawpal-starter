import pytest

from pawpal_system import Pet, Task


def test_pet_starts_with_no_tasks():
    pet = Pet("Mochi", "dog")

    assert pet.name == "Mochi"
    assert pet.species == "dog"
    assert pet.tasks == []


def test_add_task_adds_task_to_pet():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 20, "daily", "high")

    pet.add_task(task)

    assert pet.tasks == [task]


def test_edit_task_replaces_task_at_index():
    pet = Pet("Mochi", "dog")
    original_task = Task("Short walk", 10, "daily", "medium")
    updated_task = Task("Long walk", 30, "daily", "high")
    pet.add_task(original_task)

    pet.edit_task(0, updated_task)

    assert pet.tasks == [updated_task]


def test_edit_task_raises_index_error_for_missing_task():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 20, "daily", "high")

    with pytest.raises(IndexError):
        pet.edit_task(0, task)
