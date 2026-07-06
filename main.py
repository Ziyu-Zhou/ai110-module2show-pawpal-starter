from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a labeled list of tasks for the terminal demo."""
    print(f"\n{title}")
    print("-" * len(title))
    for task in tasks:
        status = "complete" if task.completed else "incomplete"
        print(
            f"- {task.description}: {task.duration_minutes} min "
            f"({status})"
        )


def main() -> None:
    owner = Owner("Jordan", "walk")

    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    # Add tasks in mixed duration order to demonstrate sorting.
    dog.add_task(
        Task(
            "Brush Mochi's fur",
            15,
            "weekly",
            "low",
            completed=True,
        )
    )
    dog.add_task(
        Task(
            "Mochi's morning walk",
            20,
            "daily",
            "high",
            start_time="08:00",
        )
    )
    cat.add_task(
        Task(
            "Feed Luna breakfast",
            10,
            "daily",
            "high",
            start_time="08:00",
        )
    )
    cat.add_task(Task("Give Luna medicine", 5, "daily", "high"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(45)

    all_tasks = owner.get_all_tasks()
    print_tasks("Tasks in insertion order", all_tasks)
    print_tasks(
        "Tasks sorted shortest to longest",
        scheduler.sort_by_time(all_tasks),
    )
    print_tasks(
        "Incomplete tasks",
        scheduler.filter_tasks(owner, completed=False),
    )
    print_tasks(
        "Mochi's tasks",
        scheduler.filter_tasks(owner, pet_name="Mochi"),
    )
    print_tasks(
        "Luna's incomplete tasks",
        scheduler.filter_tasks(
            owner,
            completed=False,
            pet_name="Luna",
        ),
    )

    scheduler.generate_schedule(owner)

    print("\nToday's Schedule")
    print("----------------")
    print(scheduler.format_daily_plan(owner))

    print("\nConflict warnings")
    print("-----------------")
    if scheduler.conflict_warnings:
        for warning in scheduler.conflict_warnings:
            print(f"- {warning}")
    else:
        print("- No scheduling conflicts found.")

    print("\nWhy this schedule?")
    for explanation in scheduler.explain_schedule():
        print(f"- {explanation}")


if __name__ == "__main__":
    main()
