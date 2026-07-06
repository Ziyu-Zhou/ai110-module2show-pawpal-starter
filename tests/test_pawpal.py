from pawpal_system import Pet, Task


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
