class Owner:
    def __init__(self, name: str, preferences: str):
        self.name = name
        self.preferences = preferences
        self.pets: list[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        pass


class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks: list[Task] = []

    def add_task(self, task: "Task") -> None:
        pass

    def edit_task(self, index: int, task: "Task") -> None:
        pass


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority


class Scheduler:
    def __init__(self, available_minutes: int):
        self.available_minutes = available_minutes
        self.scheduled_tasks: list[Task] = []

    def generate_schedule(self, tasks: list[Task]) -> list[Task]:
        pass

    def explain_schedule(self) -> list[str]:
        pass
