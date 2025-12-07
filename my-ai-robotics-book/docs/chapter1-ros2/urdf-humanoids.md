# URDF for Humanoids

Universal Robot Description Format (URDF) is an XML format used in ROS to describe all elements of a robot. It allows you to represent the robot's kinematic and dynamic properties, visual appearance, and collision geometry. For humanoid robots, URDF is crucial for defining complex joint structures and links that mimic human anatomy.

## URDF Structure

A URDF file defines a robot as a tree structure of **links** and **joints**.

-   **Link**: Represents a rigid body of the robot (e.g., torso, upper arm, forearm).
-   **Joint**: Defines the kinematic and dynamic properties between two links (e.g., revolute, prismatic, fixed).

```xml
<robot name="humanoid_robot">
  <link name="base_link">
    <!-- visual and collision properties -->
  </link>

  <link name="torso_link">
    <!-- visual and collision properties -->
  </link>

  <joint name="base_to_torso" type="revolute">
    <parent link="base_link"/>
    <child link="torso_link"/>
    <origin xyz="0 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="10"/>
  </joint>

  <!-- ... more links and joints for arms, legs, head ... -->

</robot>
```

## Key Elements in URDF for Humanoids

### Kinematic Chains

Humanoids have complex kinematic chains to enable a wide range of motion. URDF allows for defining these chains from the base to the fingertips and toes.

### Visual and Collision Models

-   **Visual**: Defines the graphical representation of each link, often using meshes (e.g., `.stl`, `.dae`). This is what you see in simulators.
-   **Collision**: Defines the simplified geometric shape used for collision detection. This is usually a simpler shape (box, cylinder, sphere) to improve simulation performance.

### Inertial Properties

Each link needs inertial properties (mass, inertia matrix) for accurate physics simulation. These are critical for humanoid balance and dynamic control.

### Joint Limits and Dynamics

URDF specifies joint limits (upper, lower, velocity, effort) to ensure realistic robot movement and prevent self-collision or damage. Joint dynamics (friction, damping) can also be defined.

## Using URDF in ROS 2

URDF files are typically loaded into the ROS 2 parameter server and used by various ROS 2 tools:

-   **`robot_state_publisher`**: Publishes the robot's state (joint positions) to the `tf` (transform) tree.
-   **RViz**: A 3D visualizer that uses URDF to display the robot model.
-   **Gazebo**: A physics simulator that can load URDF models for realistic simulation.

Creating an accurate and complete URDF for a humanoid robot is the first step towards simulating and controlling its complex movements.
