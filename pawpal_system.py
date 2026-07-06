from datetime import date, datetime, timedelta


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
        due_date: date | None = None,
        start_time: str | None = None,
    ):
        """Initialize and validate a pet care task."""
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than zero")

        normalized_priority = priority.lower()
        if normalized_priority not in self.VALID_PRIORITIES:
            raise ValueError("priority must be 'low', 'medium', or 'high'")

        normalized_start_time = None
        if start_time is not None:
            try:
                parsed_start_time = datetime.strptime(start_time, "%H:%M")
            except ValueError as error:
                raise ValueError(
                    "start_time must use HH:MM format"
                ) from error
            normalized_start_time = parsed_start_time.strftime("%H:%M")

        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = normalized_priority
        self.completed = completed
        self.due_date = due_date or date.today()
        self.start_time = normalized_start_time

    def mark_complete(self) -> "Task | None":
        """Complete this task and return its next recurring occurrence."""
        if self.completed:
            return None

        self.completed = True

        recurrence_days = {
            "daily": 1,
            "weekly": 7,
        }.get(self.frequency.lower())
        if recurrence_days is None:
            return None

        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            due_date=self.due_date + timedelta(days=recurrence_days),
            start_time=self.start_time,
        )


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
        self.conflict_warnings: list[str] = []

    def sort_by_time(
        self,
        tasks: list[Task],
        shortest_first: bool = True,
    ) -> list[Task]:
        """Return tasks sorted by their duration without changing the input."""
        return sorted(
            tasks,
            key=lambda task: task.duration_minutes,
            reverse=not shortest_first,
        )

    def filter_tasks(
        self,
        owner: Owner,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks matching an optional completion status and pet name."""
        normalized_pet_name = (
            pet_name.strip().casefold()
            if pet_name is not None
            else None
        )

        return [
            task
            for pet in owner.pets
            if (
                normalized_pet_name is None
                or pet.name.casefold() == normalized_pet_name
            )
            for task in pet.tasks
            if completed is None or task.completed is completed
        ]

    def complete_task(self, pet: Pet, task: Task) -> Task | None:
        """Complete a pet's task and add its next occurrence when recurring."""
        if task not in pet.tasks:
            raise ValueError("task does not belong to this pet")

        next_occurrence = task.mark_complete()
        if next_occurrence is not None:
            pet.add_task(next_occurrence)

        return next_occurrence

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return warnings for scheduled tasks whose time ranges overlap."""
        warnings = []

        for index, first_task in enumerate(self.scheduled_tasks):
            first_start = datetime.strptime(
                self.scheduled_start_times[first_task],
                "%H:%M",
            )
            first_end = first_start + timedelta(
                minutes=first_task.duration_minutes
            )

            for second_task in self.scheduled_tasks[index + 1:]:
                second_start = datetime.strptime(
                    self.scheduled_start_times[second_task],
                    "%H:%M",
                )
                second_end = second_start + timedelta(
                    minutes=second_task.duration_minutes
                )

                overlap_start = max(first_start, second_start)
                overlap_end = min(first_end, second_end)
                if overlap_start >= overlap_end:
                    continue

                first_pet = self._find_pet_for_task(owner, first_task)
                second_pet = self._find_pet_for_task(owner, second_task)
                first_label = (
                    first_pet.name if first_pet is not None else "Unknown pet"
                )
                second_label = (
                    second_pet.name
                    if second_pet is not None
                    else "Unknown pet"
                )
                warnings.append(
                    f"Warning: '{first_task.description}' ({first_label}) "
                    f"conflicts with '{second_task.description}' "
                    f"({second_label}) from "
                    f"{overlap_start.strftime('%H:%M')} to "
                    f"{overlap_end.strftime('%H:%M')}."
                )

        return warnings

    def generate_schedule(self, owner: Owner) -> list[Task]:
        """Generate a prioritized schedule for all of an owner's pets."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.explanations = []
        self.scheduled_start_times = {}
        self.conflict_warnings = []

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
                task_start = (
                    datetime.strptime(task.start_time, "%H:%M")
                    if task.start_time is not None
                    else current_time
                )
                self.scheduled_start_times[task] = task_start.strftime("%H:%M")
                remaining_minutes -= task.duration_minutes
                task_end = task_start + timedelta(
                    minutes=task.duration_minutes
                )
                current_time = max(current_time, task_end)

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

        self.conflict_warnings = self.detect_conflicts(owner)
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
