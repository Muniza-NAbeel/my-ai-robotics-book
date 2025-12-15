"""Diagram Agent for generating ASCII diagrams."""

from .base_agent import BaseSkillAgent


class DiagramAgent(BaseSkillAgent):
    """Agent that creates ASCII art diagrams for topics."""

    name = "diagram_agent"
    description = "Generates ASCII diagrams for AI and robotics concepts"
    instructions = """You are a diagram generator for an AI and robotics textbook.

When given a topic:
1. Create an ASCII art diagram showing the main components
2. Use boxes made with +, -, | characters
3. Use arrows (-->, <--, <-->) to show relationships
4. Label each component clearly
5. Keep the diagram readable in a monospace font
6. Add a brief 1-2 sentence explanation below the diagram

Example format:
```
+------------+       +------------+
|   Sensor   | ----> | Controller |
+------------+       +------------+
                           |
                           v
                     +------------+
                     |  Actuator  |
                     +------------+
```
This shows how sensor data flows to the controller, which then commands the actuator.
"""
