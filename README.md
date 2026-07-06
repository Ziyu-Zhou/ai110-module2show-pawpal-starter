# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- **Multi-pet planning:** Combines care tasks from every pet into one daily
  plan.
- **Smart task ordering:** Ranks tasks by priority and favors tasks matching
  the owner's preferences when priorities are equal.
- **Available-time scheduling:** Schedules incomplete tasks that fit within the
  remaining time and explains why others were skipped.
- **Sorting and filtering:** Sorts tasks by duration and filters them by pet or
  completion status.
- **Recurring tasks:** Creates the next daily or weekly task after completion
  without producing duplicates.
- **Conflict detection:** Detects overlapping fixed-time tasks while allowing
  back-to-back tasks.
- **Clear Streamlit results:** Displays tasks and schedules in tables with
  success messages, warnings, and scheduling explanations.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
Today's Schedule
----------------
- Mochi's morning walk (20 minutes, high priority)
- Feed Luna breakfast (10 minutes, high priority)
- Brush Mochi's fur (15 minutes, low priority)

Why this schedule?
- Scheduled 'Mochi's morning walk' because it has high priority and fits the available time and matches the owner's preference.
- Scheduled 'Feed Luna breakfast' because it has high priority and fits the available time.
- Scheduled 'Brush Mochi's fur' because it has low priority and fits the available time.
(.venv) prts@MichaelZhous-MacBook-Pro ai110-module2show-pawpal-starter % python main.py
Today's Schedule
----------------
Daily plan for Jordan's pets:
  08:00 — Mochi: Mochi's morning walk (20 min) [priority: high]
  08:20 — Luna: Feed Luna breakfast (10 min) [priority: high]
  08:30 — Mochi: Brush Mochi's fur (15 min) [priority: low]

Why this schedule?
- Scheduled 'Mochi's morning walk' because it has high priority and fits the available time and matches the owner's preference.
- Scheduled 'Feed Luna breakfast' because it has high priority and fits the available time.
- Scheduled 'Brush Mochi's fur' because it has low priority and fits the available time.




## Testing PawPal+
### confidence level: 4

```bash
python -m pytest
```

The automated tests cover owner and pet task management, task validation,
duration-based sorting, filtering, schedule prioritization and formatting,
daily and weekly recurrence, available-time limits, and scheduling conflict
detection.

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/prts/Documents/selflearning/codepath/ai110/ai110-module2show-pawpal-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.1
collected 40 items

tests/test_owner.py ....                                                 [ 10%]
tests/test_pawpal.py .....                                               [ 22%]
tests/test_pet.py ....                                                   [ 32%]
tests/test_scheduler.py ...................                              [ 80%]
tests/test_task.py ........                                              [100%]

============================== 40 passed in 0.04s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |


| Feature | Method(s) | Description |
|---|---|---|
| Sorting | `Scheduler.sort_by_time()` | Sorts tasks by duration. Shortest-first is the default; `shortest_first=False` sorts longest-first. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name, completion status, or both. Pet-name matching is case-insensitive. |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects overlapping task durations and returns warning messages. Back-to-back tasks are allowed. |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.complete_task()` | Creates the next daily or weekly occurrence and adds it to the same pet. One-time tasks do not recur. |


## Demo Walkthrough

### Main UI

The Streamlit interface lets a user:

- Enter an owner name and scheduling preference.
- Add multiple pets and review them in a table.
- Add care tasks with a title, duration, priority, frequency, and optional
  fixed start time.
- Filter tasks by pet or completion status and sort them by duration.
- Set the available minutes and schedule start time before generating a plan.
- Review today's schedule, skipped-task notices, conflict warnings, and an
  explanation for each scheduling decision.

### Example workflow

1. Enter the owner's details and add a pet such as Mochi.
2. Add tasks such as a morning walk, feeding, medicine, or grooming.
3. Optionally assign fixed start times to tasks that must happen at a specific
   time.
4. Use the task table controls to filter by pet or status and sort by duration.
5. Choose the available time and click **Generate schedule**.
6. Review the scheduled-task table, conflict check, and “Why this schedule?”
   explanation.

### Scheduler behaviors demonstrated

- `sort_by_time()` orders tasks from shortest to longest or longest to
  shortest without mutating the original list.
- `filter_tasks()` selects tasks by pet, completion status, or both.
- `generate_schedule()` ranks high-priority tasks first, uses the owner's
  preference to break priority ties, skips completed tasks, and respects the
  available-time limit.
- Flexible tasks are placed back-to-back, while fixed-time tasks retain their
  requested start times.
- `detect_conflicts()` compares scheduled time ranges and warns about
  overlaps. Tasks that only meet end-to-start are allowed.
- Completing daily or weekly tasks creates the next occurrence without
  duplicating an already completed occurrence.

### Sample CLI output

Run:

```bash
python main.py
```

```text
Tasks in insertion order
------------------------
- Brush Mochi's fur: 15 min (complete)
- Mochi's morning walk: 20 min (incomplete)
- Feed Luna breakfast: 10 min (incomplete)
- Give Luna medicine: 5 min (incomplete)

Tasks sorted shortest to longest
--------------------------------
- Give Luna medicine: 5 min (incomplete)
- Feed Luna breakfast: 10 min (incomplete)
- Brush Mochi's fur: 15 min (complete)
- Mochi's morning walk: 20 min (incomplete)

Incomplete tasks
----------------
- Mochi's morning walk: 20 min (incomplete)
- Feed Luna breakfast: 10 min (incomplete)
- Give Luna medicine: 5 min (incomplete)

Mochi's tasks
-------------
- Brush Mochi's fur: 15 min (complete)
- Mochi's morning walk: 20 min (incomplete)

Luna's incomplete tasks
-----------------------
- Feed Luna breakfast: 10 min (incomplete)
- Give Luna medicine: 5 min (incomplete)

Today's Schedule
----------------
Daily plan for Jordan's pets:
  08:00 — Mochi: Mochi's morning walk (20 min) [priority: high]
  08:00 — Luna: Feed Luna breakfast (10 min) [priority: high]
  08:20 — Luna: Give Luna medicine (5 min) [priority: high]

Conflict warnings
-----------------
- Warning: 'Mochi's morning walk' (Mochi) conflicts with 'Feed Luna breakfast' (Luna) from 08:00 to 08:10.

Why this schedule?
- Scheduled 'Mochi's morning walk' because it has high priority and fits the available time and matches the owner's preference.
- Scheduled 'Feed Luna breakfast' because it has high priority and fits the available time.
- Scheduled 'Give Luna medicine' because it has high priority and fits the available time.
- Skipped 'Brush Mochi's fur' because it is already complete.
```
