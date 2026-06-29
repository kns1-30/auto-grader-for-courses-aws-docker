# Auto-Grader for Courses — AWS + Docker

A cloud-based, scalable auto-grader system for introductory C++ programming courses. Students submit code through a web interface; the system compiles, executes, and scores it automatically — all inside Docker containers deployed on AWS Elastic Beanstalk.

## Architecture

```
Student Browser  →  Flask Web UI  →  Docker Container (compile + execute + compare)
                                              ↓
                                      Score & Feedback returned to browser
                                              ↓
                               AWS Elastic Beanstalk (Docker Hub image)
```

## Features

- **Compile check**: verifies the submission compiles without errors
- **Execution sandbox**: runs student code in an isolated Docker environment
- **Output comparison**: compares program output against known-correct output
- **Instant feedback**: returns score and feedback through the browser
- **Cloud deployment**: entire system packaged as a Docker container running on AWS

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web frontend | Flask (Python) |
| Grading sandbox | Docker |
| Cloud hosting | AWS Elastic Beanstalk |
| Image registry | Docker Hub |
| Target language | C++ |

## Project Breakdown

**Part 1 — Docker basics**
Getting familiar with containerization: building images, running containers, managing volumes.

**Part 2 — Auto-grader system**
Flask web server allowing students to upload `walk.cc`. The grader:
1. Attempts to compile the submission with `g++`
2. If compilation succeeds, executes the binary in a controlled environment
3. Compares stdout against the expected output
4. Returns pass/fail score with feedback

**Part 3 — AWS deployment**
Docker container pushed to Docker Hub and deployed to AWS Elastic Beanstalk for public access.

## Assignment Spec

> Write a C++ program (`walk.cc`) that prompts the user for the names of two people, then prints a statement that says those two people went on a walk together.

## Getting Started

```bash
# Build Docker image
docker build -t auto-grader .

# Run locally
docker run -p 5000:5000 auto-grader

# Visit http://localhost:5000 to submit code
```
