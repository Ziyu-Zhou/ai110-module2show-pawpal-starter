# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. Owner stores the owner’s name, preferences, and pets. add_pet() adds a pet to the owner.

2. Pet stores its name, species, and care tasks. It can add or edit tasks.

3. Task describes one care activity using a title, duration, and priority.

4. Scheduler receives tasks, selects those that fit within available_minutes, and explains its choices.


### key actions:

1. Add a pet (and owner) profile
2. Add a care task
3. Generate today's plan

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

1. Yes, perference of owner was just existing but not connnected to the scheduler, now it's updated

2. Also explain_schedule didn't quite work because it's not sure what explaination can be use which is not also updated.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

* Constraints considered: The scheduler considers task priority, the owner’s preferences, completion status, task duration, available minutes, and fixed start-time conflicts.

* How they were prioritized: Safety and essential care come first, so high-priority tasks are considered before medium- and low-priority tasks. Owner preferences break ties between tasks with the same priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The detect_conflicts method uses a nested loop to compare every scheduled
task with every task after it. This keeps the algorithm straightforward.The tradeoff is that it takes
O(n²), and repeatedly parses times and looks up pets. This is
reasonable for PawPal because an owner is likely to schedule only a small
number of pet-care tasks in one day, so readability is more valuable than a
more complex optimization.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

* I used AI throughout the project to brainstorm the class design, identify scheduling edge cases, draft automated tests, improve the Streamlit display, update the UML diagram, and refine the README documentation.

* The best prompts are telling the AI to do one very specific task.



**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

1. There was a time my prompt was probably too broad so the AI decide to write 500 line of code and I ended up reverting all of them.

2. I like to tell the AI to test everything it just did.



---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?


1. Behaviors tested: I tested task creation and validation, pet and owner task management, duration sorting, filtering by pet and completion status, priority-based scheduling, owner-preference tie-breaking, available-time limits, daily and weekly recurrence, duplicate recurrence prevention, start-time assignment, conflict detection, and schedule formatting.

2. These tests cover the scheduler’s main responsibilities and its most likely failure points.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

1. I am highly confident that the scheduler’s core behavior works correctly because all 40 automated tests pass. 

2. I would test schedules crossing midnight, duplicate pet or task names
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

* When things start coming together and the app finally worked, because there was huge chunk of time the program spent on backend only.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

* I think I will redesign the time element of the program, I like what I have not as well because it's easier to use for the user.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

* AI can be very powerful and allow a single developer to build project very fast as long as the developer know what he is trying to do.
