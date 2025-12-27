# CS50 Final project : Advanced task list application system (ATLAS)

#### Video Demo:  
[Video](https://youtu.be/fySZ8SvQBM8)

## Description

### Background

After having followed the Harvard CS50 course on [EDX.org](www.edx.org) I have decided to complete the final project.
This repository is where the code of my final project is saved.

### Summary

This advanced todo list application, is a web application (for now...) allowing the user to not only list tasks to complete, but also set estimated duration and use a timer when the user is working on the specific task, with a countdown to help staying focused on the task at end.
In this README file I will do my best to share all the resources I have used so that if someone wants to work on its own project he or she can follow my steps and access the references I share.

### Features

ATLAS has all the basic features of a standard todolist, including:

- CRUD operations on the User
- CRUD operations on the tasks
- Tasks status: new, pending, active, completed, postponed, cancelled

In addition, there are additional features, namely:

- Task estimated duration
- Countdown/timer on the active task
- Tasks groups
- Tasks sharing and assignment with other users

# Technology

## Stack

To maintain for now some simplicity the stack will be:

| Service  |    Framework   | Language   |
| :------- | :------------: | :--------- |
| Backend  |    Django      | Python     |
| Frontend |    ReactJS*    | Javascript |
| Database |    SQLite3     | SQL        |
| Hosting  | Digital Ocean* |

*to be added
## Other systems and utilities

Other systems will include:
| System type | Name |  
| :--------- | :-------: |
| Source code versioning | Github |
| CI/CD | Github Actions |
| BE Testing | unittest|
| FE testing | Jest* |  
| IDE | VS Code
| UI design | Figma

*to be added
## Techniques

Before coding anything, requirements have to be defined, and translated into user stories.
In as far as practicable I will be using test driven development (TDD) in order to secure every piece of production code.

# Development

Before starting the project I defined the thought process and the development process in order to not only properly document the whole project but also keep up with a certain work performance and efficiency.

## General Process

Although the idea is not to deliver a professional and production ready solution, I have tried to get as close to production code as practicable for me. However, I might take some shortcuts whenever I deem necessary for the sake of the project completion.

### 1. Planning & Requirements Gathering

- Define project goals and objectives.
- Identify target audience and user personas.
- Gather functional and non-functional requirements.
- Choose tech stack (Frontend, Backend, Database, Hosting, etc.).
- Define test cases for each feature.
- Choose a testing framework (Jest, Mocha, PyTest, JUnit, etc.).

### 2. System Architecture & Design

- Design system architecture (Monolithic vs. Microservices).
- Define API structures (REST, GraphQL, WebSockets).
- Choose database models (SQL vs. NoSQL).
- Plan authentication & authorization (OAuth, JWT, SSO, etc.).
- Set up CI/CD pipelines for automation.
- Define testing strategy:
  - Unit tests
  - Integration tests
  - End-to-end (E2E) tests

### 3. Development (TDD Integrated)

### Red-Green-Refactor Cycle:

1. Write a failing test (Red)
2. Write the minimum code to pass the test (Green)
3. Refactor the code while keeping tests passing

#### Frontend TDD

- Write failing tests for UI components.
- Implement minimal code to pass the test.
- Refactor UI code.

Example (React + Jest + React Testing Library):

```javascript
test('renders login button', () => {
	render(<Login />);
	expect(screen.getByText(/Login/i)).toBeInTheDocument();
});
```

#### Backend TDD

- Write failing tests for API endpoints.
- Implement minimal logic to pass tests.
- Refactor and optimize code.

Example (Node.js + Jest + Supertest):

```javascript
test('POST /login should return 200', async () => {
	const response = await request(app).post('/login').send({
		username: 'test',
		password: 'password123',
	});
	expect(response.status).toBe(200);
});
```

### 4. Testing

- Run automated test suites before merging code.
- Add edge-case tests.
- Measure test coverage using Istanbul, Coverage.py, etc.

### 5. Deployment & CI/CD

- Integrate tests into CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins).
- Prevent deployment if tests fail.

Example (GitHub Actions):

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

### 6. Post-Deployment & Maintenance

- Automate regression testing before updates.
- Monitor performance & fix bugs with additional tests.
- Optimize performance & security.

### 7. Continuous Improvement

- Analyze user behavior (Google Analytics, Hotjar).
- Plan for new features & upgrades.

### Key Benefits of TDD

✅ Fewer bugs in production  
✅ More modular and maintainable code  
✅ Confidence in refactoring without breaking functionality  
✅ Easier collaboration with well-defined test cases

## Detailed process

### Project Goals & Objectives for the Advanced To-Do List Web Application

#### Project Goals

- **Efficient Task Management** – Enable users to create, manage, and track tasks with estimated durations.
- **Time Tracking & Productivity Enhancement** – Provide countdown timers for active tasks to help users stay focused.
- **Collaboration & Task Sharing** – Allow users to assign and share tasks with teammates, improving teamwork.
- **Organized Task Grouping** – Enable users to categorize tasks into groups for better organization.
- **User-Friendly & Responsive UI** – Build an intuitive, mobile-friendly web application.
- **Secure & Scalable** – Implement robust authentication, data security, and a scalable architecture.

#### Project Objectives

**Task Management:**

- Users can create, update, delete, and mark tasks as completed.
- Each task includes an estimated duration field.

**Countdown Timer:**

- Users can start a task, triggering a real-time countdown.
- Automatically pause and resume tasks as needed.

**Task Groups:**

- Users can create and manage task categories.
- Filter tasks based on assigned groups.

**Task Sharing & Assignment:**

- Assign tasks to other users with different permission levels (Owner, Editor, Viewer).
- Notify assigned users via real-time alerts or email.

**User Authentication & Roles:**

- Secure user authentication (Django Authentication / OAuth).
- Role-based permissions for task access and management.

**Real-Time Updates:**

- WebSockets/Django Channels to handle live updates for task status and timers.

**Scalability & Performance:**

- Optimize database queries for efficiency.
- Implement caching mechanisms where needed.

### Identify Target Audience & User Personas

#### Define the Target Audience

Think about who would benefit most from your app. Some potential user groups:

- **Professionals & Teams** → Need collaboration, task assignment, and real-time tracking.
- **Students & Educators** → Need organized study plans, task prioritization, and timers.
- **Freelancers & Entrepreneurs** → Need productivity tools, time tracking, and task management.
- **General Users **→ Need personal task tracking and scheduling.

#### Create User Personas

User personas help understand users' needs and behaviors.

👤 Persona 1: Sarah (Project Manager)

- **Pain Points:** Struggles with team task tracking and deadlines.
- **Needs**: A task assignment system with notifications.
- **Features Needed**: Task sharing, permissions, real-time updates.

👤 Persona 2: John (Freelancer)

- **Pain Points:** Needs to track time spent on client projects.
- **Needs**: A task timer with estimated duration tracking.
- **Features Needed**: Countdown timer, task duration analytics.

👤 Persona 3: Emily (Student)

- **Pain Points:** Has trouble keeping track of multiple assignments.
- **Needs**: A task grouping system to organize subjects.
- **Features Needed**: Task categories, prioritization, deadline reminders.

### Functional and Non-Functional Requirements

#### Functional Requirements

1. **User Authentication**

   - Users should be able to **register** and **login** securely.
   - Passwords should be **hashed** and **encrypted**.
   - Authentication can support **OAuth** (e.g., Google login).
   - Users can **reset their password** via email.

2. **Task Management**

   - Users can **create, edit, and delete tasks**.
   - Tasks can have a **title, description, due date, priority, and status**.
   - Tasks should have an **estimated duration**.
   - Users can **mark tasks as completed** or **delete them**.

3. **Task Grouping**

   - Users can **group tasks** into categories (e.g., “Work,” “Personal,” “Study”).
   - Users can **filter** tasks based on their group or priority.

4. **Timer & Countdown**

   - Users can **start a timer** for each task (to track the time spent).
   - **Real-time countdown** shows the remaining time for an active task.
   - **Pause/Resume** functionality for tasks with active timers.

5. **Task Sharing & Assignment**

   - Users can **assign tasks to other users**.
   - Each task has **assigned roles** (Owner, Editor, Viewer).
   - **Notifications** sent when a task is assigned, updated, or completed.

6. **Task Status & Prioritization**

   - Tasks can have different statuses: **To Do, In Progress, Completed**.
   - Users can **set priority levels** (Low, Medium, High).

7. **Task Due Dates & Deadlines**

   - Users can set due dates for each task.
   - A **notification system** will remind users of upcoming deadlines.

8. **Task Search & Filtering**

   - Users can **search** for tasks by title, due date, priority, etc.
   - Users can **filter tasks** based on different criteria (e.g., due date, priority).

9. **Real-Time Collaboration**
   - Users can see live updates (tasks, timer changes) in real-time.
   - **WebSockets/Django Channels** can be used for real-time collaboration.

#### Non-Functional Requirements

1. **Performance**

   - The application should load tasks within **2 seconds**.
   - Timers should update in **real-time** without noticeable delay.

2. **Security**

   - The system must have **secure user authentication**.
   - All passwords must be **hashed** and **stored securely**.
   - **Input validation** to prevent security vulnerabilities (SQL injection, XSS, etc.).
   - **Role-based access control** for different user roles (Owner, Editor, Viewer).

3. **Scalability**

   - The application should handle up to **10,000 concurrent users**.
   - Should be able to scale horizontally to handle more users and tasks.

4. **Availability**

   - The application should have an **uptime of 99.9%**.
   - Implement **load balancing** for high availability.

5. **Usability**

   - The application must be **intuitive** and easy to use for both **novice and experienced users**.
   - The UI should be **responsive** for mobile, tablet, and desktop.
   - Include tooltips, help sections, and **onboarding guides** for new users.

6. **Maintainability**

   - The code should be **well-documented** for future maintenance and feature expansion.
   - It should support **modular design** for easy updates and additions.

7. **Backup & Recovery**

   - Regular database backups to avoid data loss.
   - The application should support **data recovery** in case of failure.

8. **Localization**

   - The system should support **multi-language support** for broader accessibility (optional).

9. **Compliance**
   - Comply with **GDPR** for handling user data (if required).
   - Implement **cookie consent** banners for legal compliance.

### Test cases for each feature

#### User Authentication

1. **User Registration**

   - **Objective**: Ensure that users can register with valid input.
   - **Steps**:
     1. Navigate to the registration page.
     2. Enter valid email, password, and username.
     3. Submit the form.
   - **Expected Result**: User should be redirected to the login page with a success message. A new user should be created in the database.

2. **User Login**

   - **Objective**: Ensure that users can log in with valid credentials.
   - **Steps**:
     1. Navigate to the login page.
     2. Enter valid email and password.
     3. Submit the form.
   - **Expected Result**: User should be logged in and redirected to the dashboard or home page.

3. **Invalid User Login**

   - **Objective**: Ensure the system rejects invalid login attempts.
   - **Steps**:
     1. Navigate to the login page.
     2. Enter invalid email or password.
     3. Submit the form.
   - **Expected Result**: An error message should be displayed, and the user should not be logged in.

4. **Password Reset**
   - **Objective**: Ensure that users can reset their passwords.
   - **Steps**:
     1. Navigate to the password reset page.
     2. Enter the registered email address.
     3. Submit the form.
   - **Expected Result**: A password reset email should be sent, and the user should be prompted to change their password.

#### Task Management

1. **Create Task**

   - **Objective**: Ensure users can create a new task.
   - **Steps**:
     1. Navigate to the task creation page.
     2. Enter a title, description, due date, priority, and estimated duration.
     3. Click the "Create" button.
   - **Expected Result**: Task is saved to the database and displayed in the task list.

2. **Edit Task**

   - **Objective**: Ensure users can edit an existing task.
   - **Steps**:
     1. Navigate to an existing task.
     2. Click "Edit" and modify the title, description, due date, etc.
     3. Save the changes.
   - **Expected Result**: Task is updated with the new information in the database.

3. **Delete Task**
   - **Objective**: Ensure users can delete a task.
   - **Steps**:
     1. Navigate to the task you want to delete.
     2. Click the "Delete" button.
     3. Confirm the deletion.
   - **Expected Result**: Task is deleted from the database and removed from the task list.

#### Task Grouping

1. **Create Task Group**

   - **Objective**: Ensure users can create a task group.
   - **Steps**:
     1. Navigate to the task group page.
     2. Click the "Create Group" button.
     3. Enter a group name and description.
     4. Save the group.
   - **Expected Result**: Task group is created and displayed in the task group list.

2. **Assign Task to Group**
   - **Objective**: Ensure tasks can be assigned to a group.
   - **Steps**:
     1. Navigate to an existing task.
     2. Select a group from a dropdown menu.
     3. Save the changes.
   - **Expected Result**: Task is associated with the selected group, and the task is listed under the group.

#### Timer & Countdown

1. **Start Timer**

   - **Objective**: Ensure the timer starts correctly when a task is active.
   - **Steps**:
     1. Navigate to an active task.
     2. Click the "Start Timer" button.
   - **Expected Result**: The timer should start counting down from the estimated duration.

2. **Pause Timer**

   - **Objective**: Ensure the timer can be paused.
   - **Steps**:
     1. Start the timer.
     2. Click the "Pause" button.
   - **Expected Result**: The timer should stop, and the time elapsed should be saved.

3. **Resume Timer**
   - **Objective**: Ensure the timer can be resumed after being paused.
   - **Steps**:
     1. Pause the timer.
     2. Click the "Resume" button.
   - **Expected Result**: The timer should resume from where it was paused.

#### Task Sharing & Assignment

1. **Assign Task to Another User**

   - **Objective**: Ensure tasks can be assigned to another user.
   - **Steps**:
     1. Navigate to a task.
     2. Select a user from the "Assign" dropdown.
     3. Click "Save."
   - **Expected Result**: The task is assigned to the selected user, and they receive a notification.

2. **Task Notification**
   - **Objective**: Ensure users are notified when a task is assigned to them.
   - **Steps**:
     1. Assign a task to a user.
     2. Verify that the assigned user receives a notification about the task.
   - **Expected Result**: The assigned user should receive a notification, and the task should be added to their task list.

#### Task Status & Prioritization

1. **Set Task Priority**

   - **Objective**: Ensure users can set the priority of a task.
   - **Steps**:
     1. Navigate to a task.
     2. Select a priority level (Low, Medium, High).
     3. Save the changes.
   - **Expected Result**: Task should be updated with the selected priority level.

2. **Change Task Status**
   - **Objective**: Ensure users can change the status of a task.
   - **Steps**:
     1. Navigate to a task.
     2. Change the status (To Do, In Progress, Completed).
     3. Save the changes.
   - **Expected Result**: The status should be updated, and the task should be displayed under the new status category.

#### Task Due Dates & Deadlines

1. **Set Due Date for Task**

   - **Objective**: Ensure users can set a due date for a task.
   - **Steps**:
     1. Navigate to a task.
     2. Select a due date.
     3. Save the task.
   - **Expected Result**: Task should be displayed with the selected due date.

2. **Deadline Reminder Notification**
   - **Objective**: Ensure users are notified about upcoming task deadlines.
   - **Steps**:
     1. Set a due date for a task.
     2. Wait for the reminder time to trigger.
   - **Expected Result**: A reminder notification should be sent when the task is close to its deadline.

#### Task Search & Filtering

1. **Search Task by Title**

   - **Objective**: Ensure users can search tasks by title.
   - **Steps**:
     1. Enter a task title in the search bar.
     2. Submit the search.
   - **Expected Result**: Tasks with the matching title should be displayed.

2. **Filter Tasks by Priority**
   - **Objective**: Ensure users can filter tasks by priority.
   - **Steps**:
     1. Select a priority filter (Low, Medium, High).
     2. Submit the filter.
   - **Expected Result**: Only tasks with the selected priority level should be displayed.

# References

## Resources

Django Test Driven Development [video](https://www.youtube.com/watch?v=REhBTwubGzo&t=187s)

## Credits
[django](https://www.djangoproject.com/)  
Main framework for the development of this project.  
[github](https://github.com/)  
Hosting of the code. Github copilot was also used on VS Code when needed to accelerate the writing, particularly for test functions.  
[claude.ai](https://claude.ai)  
Used for formulation of some tests during TDD process and debugging of some implementation errors. In addition, it was used to support the writing of the public pages.  
[chatgpt.com](https://chatgpt.com)  
Used for README.md file initial writing and review as well as for deployment errors troubleshouting.
