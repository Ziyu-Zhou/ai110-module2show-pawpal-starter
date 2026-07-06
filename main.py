from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", "walk")

    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    dog.add_task(Task("Mochi's morning walk", 20, "daily", "high"))
    dog.add_task(Task("Brush Mochi's fur", 15, "weekly", "low"))
    cat.add_task(Task("Feed Luna breakfast", 10, "daily", "high"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(45)
    scheduler.generate_schedule(owner)

    print("Today's Schedule")
    print("----------------")
    print(scheduler.format_daily_plan(owner))

    print("\nWhy this schedule?")
    for explanation in scheduler.explain_schedule():
        print(f"- {explanation}")


if __name__ == "__main__":
    main()
