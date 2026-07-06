from datetime import datetime, timedelta


class Owner:
    def __init__(self, name: str, preferences: str):
        """Initialize an owner with preferences and an empty pet list."""
        self.name = name
        self.preferences = preferences
        self.pets: list[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list["Task"]:
        """Return all tasks belonging to all of the owner's pets."""
        return [
            task
            for pet in self.pets
            for task in pet.tasks
        ]


class Pet:
    def __init__(self, name: str, species: str):
        """Initialize a pet with an empty task list."""
        self.name = name
        self.species = species
        self.tasks: list[Task] = []

    def add_task(self, task: "Task") -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def edit_task(self, index: int, task: "Task") -> None:
        """Replace the task at the given index."""
        self.tasks[index] = task


class Task:
    VALID_PRIORITIES = {"low", "medium", "high"}

    def __init__(
        self,
        description: str,
        duration_minutes: int,
        frequency: str,
        priority: str,
        completed: bool = False,
    ):
        """Initialize and validate a pet care task."""
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than zero")

        normalized_priority = priority.lower()
        if normalized_priority not in self.VALID_PRIORITIES:
            raise ValueError("priority must be 'low', 'medium', or 'high'")

        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = normalized_priority
        self.completed = completed

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(
        self, available_minutes: int, start_time: str = "08:00"
    ):
        """Initialize a scheduler with its time limit and start time."""
        if available_minutes < 0:
            raise ValueError("available_minutes cannot be negative")

        try:
            parsed_start_time = datetime.strptime(start_time, "%H:%M")
        except ValueError as error:
            raise ValueError("start_time must use HH:MM format") from error

        self.available_minutes = available_minutes
        self.start_time = parsed_start_time.strftime("%H:%M")
        self.scheduled_tasks: list[Task] = []
        self.skipped_tasks: list[Task] = []
        self.explanations: list[str] = []
        self.scheduled_start_times: dict[Task, str] = {}

    def generate_schedule(self, owner: Owner) -> list[Task]:
        """Generate a prioritized schedule for all of an owner's pets."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.explanations = []
        self.scheduled_start_times = {}

        preferences = owner.preferences.strip().lower()
        tasks = sorted(
            owner.get_all_tasks(),
            key=lambda task: (
                self.PRIORITY_ORDER[task.priority],
                not self._matches_preference(task, preferences),
            ),
        )

        remaining_minutes = self.available_minutes
        current_time = datetime.strptime(self.start_time, "%H:%M")

        for task in tasks:
            if task.completed:
                self.skipped_tasks.append(task)
                self.explanations.append(
                    f"Skipped '{task.description}' because it is already complete."
                )
            elif task.duration_minutes <= remaining_minutes:
                self.scheduled_tasks.append(task)
                self.scheduled_start_times[task] = current_time.strftime(
                    "%H:%M"
                )
                remaining_minutes -= task.duration_minutes
                current_time += timedelta(minutes=task.duration_minutes)

                reason = f"it has {task.priority} priority and fits the available time"
                if self._matches_preference(task, preferences):
                    reason += " and matches the owner's preference"
                self.explanations.append(
                    f"Scheduled '{task.description}' because {reason}."
                )
            else:
                self.skipped_tasks.append(task)
                self.explanations.append(
                    f"Skipped '{task.description}' because only "
                    f"{remaining_minutes} minutes remain."
                )

        return self.scheduled_tasks.copy()

    def explain_schedule(self) -> list[str]:
        """Return explanations for scheduled and skipped tasks."""
        return self.explanations.copy()

    def format_daily_plan(self, owner: Owner) -> str:
        """Format the generated schedule as a readable daily plan."""
        if len(owner.pets) == 1:
            pet = owner.pets[0]
            header = f"Daily plan for {pet.name} ({pet.species.title()}):"
        else:
            header = f"Daily plan for {owner.name}'s pets:"

        lines = [header]

        if not self.scheduled_tasks:
            lines.append("  No tasks scheduled.")
            return "\n".join(lines)

        for task in self.scheduled_tasks:
            pet = self._find_pet_for_task(owner, task)
            pet_label = (
                f"{pet.name}: "
                if len(owner.pets) > 1 and pet is not None
                else ""
            )
            lines.append(
                f"  {self.scheduled_start_times[task]} — "
                f"{pet_label}{task.description} "
                f"({task.duration_minutes} min) "
                f"[priority: {task.priority}]"
            )

        return "\n".join(lines)

    @staticmethod
    def _matches_preference(task: Task, preferences: str) -> bool:
        """Return whether a task description matches owner preferences."""
        return bool(
            preferences
            and preferences in task.description.lower()
        )

    @staticmethod
    def _find_pet_for_task(owner: Owner, task: Task) -> Pet | None:
        """Find the owner's pet associated with a task."""
        for pet in owner.pets:
            if task in pet.tasks:
                return pet
        return None
