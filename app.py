from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
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

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

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
        )
        selected_pet.add_task(task)
        st.session_state.pop("scheduler", None)
        st.success(f"Added '{cleaned_title}' for {selected_pet.name}.")

task_rows = [
    {
        "pet": pet.name,
        "task": task.description,
        "duration_minutes": task.duration_minutes,
        "frequency": task.frequency,
        "priority": task.priority,
    }
    for pet in owner.pets
    for task in pet.tasks
]

if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
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
    st.code(
        scheduler.format_daily_plan(owner),
        language="text",
    )

    with st.expander("Why this schedule?"):
        for explanation in scheduler.explain_schedule():
            st.write(f"- {explanation}")
