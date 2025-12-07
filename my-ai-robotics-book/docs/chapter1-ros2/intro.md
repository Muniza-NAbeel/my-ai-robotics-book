# Chapter 1: Learning ROS 2 Fundamentals

Welcome to Chapter 1: "Learning ROS 2 Fundamentals"! In this module, you will dive into the Robot Operating System 2 (ROS 2), a flexible framework for writing robot software. ROS 2 is widely used in research and industry for building complex robotic applications.

## What You Will Learn

This module will introduce you to the core concepts of ROS 2 and its application in robotics using Python. You will understand how ROS 2 components interact and how to develop basic robotic behaviors.

### Key Topics in this Module:

-   **ROS 2 Architecture**: Understanding the structure of ROS 2, including nodes, topics, services, and actions.
-   **Python and `rclpy`**: Developing ROS 2 applications using the Python client library `rclpy`.
-   **URDF for Humanoids**: Representing robot models using Universal Robot Description Format (URDF).
-   **Hands-on Exercises**: Building simple ROS 2 packages and simulating basic robot interactions.

By the end of this module, you will be able to identify ROS 2 components and understand how to integrate `rclpy` for Python-based robot programming. Let's get started!

## Exercises

1.  **Create a Simple ROS 2 Package**: Follow the ROS 2 documentation to create a new Python package.
2.  **Implement a Basic Publisher**: Inside your new package, create a Python node that publishes a "Hello World" string to a topic every second.
3.  **Implement a Basic Subscriber**: Create another Python node in the same package that subscribes to the topic from Exercise 2 and prints the received messages.
4.  **Run the Nodes**: Compile your package and run both the publisher and subscriber nodes simultaneously to observe the communication.
