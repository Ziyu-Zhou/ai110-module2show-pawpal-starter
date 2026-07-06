from pawpal_system import Owner, Pet, Task


def test_owner_starts_with_no_pets():
    owner = Owner("Jordan", "Morning care preferred")

    assert owner.name == "Jordan"
    assert owner.preferences == "Morning care preferred"
    assert owner.pets == []


def test_add_pet_adds_pet_to_owner():
    owner = Owner("Jordan", "Morning care preferred")
    pet = Pet("Mochi", "dog")

    owner.add_pet(pet)

    assert owner.pets == [pet]


def test_get_all_tasks_returns_tasks_from_every_pet():
    owner = Owner("Jordan", "Morning care preferred")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    walk = Task("Morning walk", 20, "daily", "high")
    feeding = Task("Breakfast", 10, "daily", "high")
    grooming = Task("Brush fur", 15, "weekly", "medium")
    dog.tasks = [walk, feeding]
    cat.tasks = [grooming]
    owner.add_pet(dog)
    owner.add_pet(cat)

    tasks = owner.get_all_tasks()

    assert tasks == [walk, feeding, grooming]


def test_get_all_tasks_returns_empty_list_when_owner_has_no_pets():
    owner = Owner("Jordan", "Morning care preferred")

    assert owner.get_all_tasks() == []
