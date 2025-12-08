# Project Goals

1. Develop a new service for conducting Live Coding Interviews from scratch
2. Write tests for frontend and backend
3. Package the solution into publishable containers
4. Develop CI/CD pipeline for GitHub Actions with tests and deployment
5. Publish the solution on free hosting

# Technology Stack

**Frontend** - Vue.js
**Backend** - Python FastAPI, using UV as Python package manager
**Database** - PostgreSQL

# Requirements

The service has two types of users: interviewer and candidate

## Interviewer Requirements

1. Login to the system, provide full name
2. Select tasks for the candidate
   - Choose difficulty level, programming language, and number of tasks
3. Start Live Coding session
   - A link for the candidate is generated when starting the session
4. After candidate connects, interviewer should see:
   1. Code editor where candidate types code with syntax highlighting
   2. Candidate's full name
   3. Current task description
   4. Current task number and remaining tasks count
   5. Code execution results
5. End Live Coding session
6. After completion, evaluate each task's solution and leave comments

## Candidate Requirements

1. Receive invitation link
2. Enter full name
3. Join Live Coding session
4. After connecting, candidate should see:
   1. Code editor with syntax highlighting
   2. Interviewer's full name
   3. Current task description
   4. Current task number and remaining tasks count
   5. Ability to run code
5. After session completion, see thank you message with a wise quote

# MVP Scope

1. Interface must be in English
2. First version supports Python only
3. First version includes 3 tasks for each difficulty level: Junior, Middle, Senior 