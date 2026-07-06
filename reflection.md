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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The `detect_conflicts()` method uses a nested loop to compare every scheduled
task with every task after it. This keeps the algorithm straightforward and
allows it to detect partial overlaps using each task's start time and duration,
not only tasks with identical start times. The tradeoff is that it takes
quadratic time, or O(n²), and repeatedly parses times and looks up pets. This is
reasonable for PawPal because an owner is likely to schedule only a small
number of pet-care tasks in one day, so readability is more valuable than a
more complex optimization. If the app needed to handle hundreds of tasks, the
algorithm could precompute each task's time interval and pet name, sort the
intervals by start time, and compare only intervals that could still overlap.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
