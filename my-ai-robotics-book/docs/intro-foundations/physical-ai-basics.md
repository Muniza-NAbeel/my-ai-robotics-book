# Python Basics for AI & Robotics

Python is the language of choice for many AI and robotics projects due to its simplicity, extensive libraries, and large community. This section will cover the fundamental Python concepts you'll need to get started.

## Variables and Data Types

Python supports various data types such as integers, floats, strings, and booleans.

```python
# Integers
x = 10

# Floats
y = 10.5

# Strings
name = "Alice"

# Booleans
is_robot = True
```

## Lists and Dictionaries

Lists are ordered collections, and dictionaries are unordered key-value pairs.

```python
# Lists
robot_sensors = ["LiDAR", "Camera", "IMU"]

# Dictionaries
robot_config = {
    "model": "Humanoid-V1",
    "motors": 12,
    "battery": "LiPo"
}
```

## Control Flow

Conditional statements (`if`, `elif`, `else`) and loops (`for`, `while`) are essential for controlling program execution.

```python
# Conditional statement
if is_robot:
    print("It is a robot.")
else:
    print("It is not a robot.")

# For loop
for sensor in robot_sensors:
    print(f"Sensor: {sensor}")

# While loop
i = 0
while i < 3:
    print(f"Iteration {i}")
    i += 1
```

## Functions

Functions allow you to encapsulate reusable blocks of code.

```python
def greet(name):
    return f"Hello, {name}!"

message = greet("World")
print(message)


def calculate_force(mass, acceleration):
    return mass * acceleration

force = calculate_force(10, 9.8)
print(f"Force: {force} Newtons")
```

<!-- Placeholder for diagrams explaining data types or control flow -->
<!-- Placeholder for more complex Python examples for robotics -->
<!-- Placeholder for external references to Python documentation or tutorials -->
