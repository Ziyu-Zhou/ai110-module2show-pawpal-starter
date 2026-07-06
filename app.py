from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planner that organizes tasks around your
available time, priorities, and preferences.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What PawPal+ can do"):
    st.markdown(
        """
- Track care tasks for multiple pets
- Sort and filter tasks for a clearer overview
- Build a prioritized daily plan within your available time
- Flag overlapping task times and explain scheduling decisions
"""
    )

st.divider()

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value="Jordan")
preferences = st.text_input(
    "Scheduling preference",
    placeholder="For example: walk",
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, preferences)

owner = st.session_state.owner
owner.name = owner_name
owner.preferences = preferences

if st.button("Add pet"):
    cleaned_pet_name = pet_name.strip()
    if not cleaned_pet_name:
        st.warning("Enter a pet name before adding a pet.")
    elif any(pet.name == cleaned_pet_name for pet in owner.pets):
        st.warning(f"{cleaned_pet_name} has already been added.")
    else:
        owner.add_pet(Pet(cleaned_pet_name, species))
        st.session_state.pop("scheduler", None)
        st.success(f"Added {cleaned_pet_name}.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Choose a pet and add care tasks for the scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col1, col2 = st.columns(2)
with col1:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
with col2:
    use_fixed_time = st.checkbox(
        "Set a fixed start time",
        help="Tasks with overlapping fixed times will trigger a warning.",
    )

task_start_time = None
if use_fixed_time:
    task_start_time = st.time_input(
        "Task start time",
        value=time(8, 0),
    )

selected_pet = None
if owner.pets:
    selected_pet_name = st.selectbox(
        "Pet for this task",
        [pet.name for pet in owner.pets],
        format_func=lambda name: (
            f"{name} "
            f"({next(pet.species for pet in owner.pets if pet.name == name)})"
        ),
    )
    selected_pet = next(
        pet for pet in owner.pets
        if pet.name == selected_pet_name
    )

if st.button("Add task"):
    cleaned_title = task_title.strip()
    if selected_pet is None:
        st.warning("Add a pet before adding tasks.")
    elif not cleaned_title:
        st.warning("Enter a task title before adding the task.")
    else:
        task = Task(
            cleaned_title,
            int(duration),
            frequency,
            priority,
            start_time=(
                task_start_time.strftime("%H:%M")
                if task_start_time is not None
                else None
            ),
        )
        selected_pet.add_task(task)
        st.session_state.pop("scheduler", None)
        st.success(f"Added '{cleaned_title}' for {selected_pet.name}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks")
    filter_col, status_col, sort_col = st.columns(3)
    with filter_col:
        pet_filter = st.selectbox(
            "Filter by pet",
            ["All pets", *[pet.name for pet in owner.pets]],
        )
    with status_col:
        status_filter = st.selectbox(
            "Filter by status",
            ["All tasks", "Incomplete", "Completed"],
        )
    with sort_col:
        sort_order = st.selectbox(
            "Sort by duration",
            ["Shortest first", "Longest first"],
        )

    completed_filter = {
        "All tasks": None,
        "Incomplete": False,
        "Completed": True,
    }[status_filter]
    display_scheduler = Scheduler(0)
    filtered_tasks = display_scheduler.filter_tasks(
        owner,
        completed=completed_filter,
        pet_name=None if pet_filter == "All pets" else pet_filter,
    )
    sorted_tasks = display_scheduler.sort_by_time(
        filtered_tasks,
        shortest_first=sort_order == "Shortest first",
    )
    task_to_pet = {
        task: pet.name
        for pet in owner.pets
        for task in pet.tasks
    }
    task_rows = [
        {
            "Pet": task_to_pet[task],
            "Task": task.description,
            "Duration": f"{task.duration_minutes} min",
            "Frequency": task.frequency.title(),
            "Priority": task.priority.title(),
            "Status": "Completed" if task.completed else "Incomplete",
            "Fixed time": task.start_time or "Flexible",
        }
        for task in sorted_tasks
    ]

    if task_rows:
        st.table(task_rows)
        st.caption(
            f"Showing {len(task_rows)} of {len(all_tasks)} tasks, "
            f"{sort_order.lower()}."
        )
    else:
        st.info("No tasks match the selected filters.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Set your available time and generate a back-to-back daily plan.")

col1, col2 = st.columns(2)
with col1:
    available_minutes = st.number_input(
        "Available time (minutes)",
        min_value=0,
        max_value=1440,
        value=60,
    )
with col2:
    schedule_start = st.time_input(
        "Schedule start time",
        value=time(8, 0),
    )

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(
            int(available_minutes),
            schedule_start.strftime("%H:%M"),
        )
        scheduler.generate_schedule(owner)
        st.session_state.scheduler = scheduler

if "scheduler" in st.session_state:
    scheduler = st.session_state.scheduler
    if scheduler.scheduled_tasks:
        scheduled_minutes = sum(
            task.duration_minutes
            for task in scheduler.scheduled_tasks
        )
        st.success(
            f"Scheduled {len(scheduler.scheduled_tasks)} "
            f"{'task' if len(scheduler.scheduled_tasks) == 1 else 'tasks'} "
            f"in {scheduled_minutes} minutes."
        )
        scheduled_task_to_pet = {
            task: pet.name
            for pet in owner.pets
            for task in pet.tasks
        }
        schedule_rows = [
            {
                "Start": scheduler.scheduled_start_times[task],
                "Pet": scheduled_task_to_pet.get(task, "Unknown"),
                "Task": task.description,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority.title(),
            }
            for task in scheduler.scheduled_tasks
        ]
        st.table(schedule_rows)
    else:
        st.warning("No tasks fit the current schedule settings.")

    st.markdown("#### Conflict check")
    if scheduler.conflict_warnings:
        for warning in scheduler.conflict_warnings:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")

    if scheduler.skipped_tasks:
        st.warning(
            f"{len(scheduler.skipped_tasks)} "
            f"{'task was' if len(scheduler.skipped_tasks) == 1 else 'tasks were'} "
            "not scheduled."
        )

    with st.expander("Why this schedule?"):
        for explanation in scheduler.explain_schedule():
            st.write(f"- {explanation}")
