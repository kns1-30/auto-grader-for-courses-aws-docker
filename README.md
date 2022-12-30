# auto-grader-for-courses-aws-docker
cloud-based, scalable auto-grader system for introductory programming courses
An autograder to grade if student's code output's correct response for c++ programming language.
This project will auto-grade following student assignment: Write a C++ program called ‘walk.cc’ that prompts the user for the names of
two people, and then prints to the screen a statement that says that these two people went on a walk together.

Part 1: Getting familiar with Docker

Part 2: Auto-grader basic system
Created a Web-server-based system that makes the student submit their ‘walk.cc’ program. The code auto-grades it, and provide the score and
feedback through the browser. An auto-grader first confirms the program compiles; if it does, then the
student submission is executed under a controlled environment and compared against known output. The “compile/execute” script and “compare against known
output” script is created for determining the correctness of student submission. And flask is used for front-end:- to allow students to upload and check the results. Entire system is packaged into docker container.

Part 3: Docker in AWS: Elastic Beanstalk
Docker container runs on AWS, used docker hub for a Docker image repo.
