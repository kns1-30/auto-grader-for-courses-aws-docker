# Design Document — Auto-Grader for Courses (AWS + Docker)

## Overview

A cloud-based, scalable auto-grader for introductory C++ programming assignments. Students upload source files through a Flask web UI; the system compiles and executes their code in an isolated Docker container and compares the output against an expected answer — returning a score and feedback instantly.

---

## System Architecture

```
┌──────────────┐    HTTP Upload     ┌───────────────────────┐
│   Student    │ ─────────────────► │   Flask Web Server    │
│   Browser    │ ◄───────────────── │   (Port 5000)         │
└──────────────┘   Score + Feedback └──────────┬────────────┘
                                               │
                                    Invokes grading pipeline
                                               │
                                               ▼
                                ┌──────────────────────────────┐
                                │     Docker Container         │
                                │  ┌────────────────────────┐  │
                                │  │  1. compile.sh         │  │
                                │  │     g++ walk.cc -o out │  │
                                │  ├────────────────────────┤  │
                                │  │  2. execute.sh         │  │
                                │  │     echo "..." | ./out │  │
                                │  ├────────────────────────┤  │
                                │  │  3. compare.sh         │  │
                                │  │     diff output expect │  │
                                │  └────────────────────────┘  │
                                └──────────────────────────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │   AWS Elastic        │
                                    │   Beanstalk          │
                                    │   (Docker platform)  │
                                    └──────────────────────┘
```

---

## Grading Pipeline

### Step 1 — Compile
```bash
g++ walk.cc -o student_output 2> compile_errors.txt
```
- If compilation fails → return `0/100` with compiler error log as feedback.
- If compilation succeeds → proceed to execution.

### Step 2 — Execute (sandboxed)
```bash
echo -e "Alice\nBob" | timeout 5 ./student_output > actual_output.txt
```
- Input is piped in; stdout is captured.
- `timeout` prevents infinite loops from hanging the grader.

### Step 3 — Compare
```bash
diff actual_output.txt expected_output.txt
```
- Exact match → `100/100` ("Correct!")
- Mismatch → `0/100` with diff output as feedback

---

## Component Breakdown

| Component | File(s) | Responsibility |
|-----------|---------|---------------|
| Web UI | Flask app (`app.py`) | File upload form, display results |
| Compile script | `compile.sh` | Compile student C++ submission |
| Execute script | `execute.sh` | Run compiled binary with test input |
| Compare script | `compare.sh` | Diff actual vs. expected output |
| Expected output | `expected_output.txt` | Ground truth for grading |
| Container | `Dockerfile` | Packages all components + g++ + Flask |

---

## Dockerfile Design

```dockerfile
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    g++ \
    python3 \
    python3-pip

RUN pip3 install flask

WORKDIR /app
COPY . .

EXPOSE 5000
CMD ["python3", "app.py"]
```

The container includes:
- `g++` for C++ compilation
- Python 3 + Flask for the web server
- All grading scripts baked into the image

---

## AWS Deployment

| Resource | Configuration |
|----------|--------------|
| Platform | AWS Elastic Beanstalk — Docker platform |
| Image registry | Docker Hub (public image) |
| Port | 5000 (mapped to Beanstalk's port 80) |

### Deploy Steps
1. Push Docker image to Docker Hub: `docker push username/auto-grader`
2. Create `Dockerrun.aws.json` pointing to the image
3. Upload to Elastic Beanstalk environment

---

## Assignment Specification

**Target program**: `walk.cc`

The student's program must:
1. Prompt for the name of person 1
2. Prompt for the name of person 2
3. Print: `{Person1} and {Person2} went on a walk together.`

**Test input**:
```
Alice
Bob
```

**Expected output**:
```
Alice and Bob went on a walk together.
```

---

## Scalability Notes

- Each grading request runs in the same container process — not isolated per-student submission. For production use, each submission should spawn an isolated container (`docker run --rm`).
- Elastic Beanstalk auto-scales horizontally based on request load, so the web tier scales independently of the grading logic.
- The current design is single-assignment; to support multiple assignments, parameterize the expected output file and grading scripts by assignment ID.
