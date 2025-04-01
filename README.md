# CS50 Final project : Advanced todo list application system (ATLAS)

## Overview

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

| Service  |   Framework   | Language   |
| :------- | :-----------: | :--------- |
| Backend  |    Django     | Python     |
| Frontend |    ReactJS    | Javascript |
| Database |    SQLite3    | SQL        |
| Hosting  | Digital Ocean |

## Other systems and utilities

Other systems will include:
| System type | Name |  
| :--------- | :-------: |
| Source code versioning | Github |
| CI/CD | Github Actions |
| BE Testing | unittest|
| FE testing | Jest |  
| IDE | VS Code
| UI design | Figma

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

## Key Benefits of TDD

✅ Fewer bugs in production
✅ More modular and maintainable code
✅ Confidence in refactoring without breaking functionality
✅ Easier collaboration with well-defined test cases

# References

## Resources
