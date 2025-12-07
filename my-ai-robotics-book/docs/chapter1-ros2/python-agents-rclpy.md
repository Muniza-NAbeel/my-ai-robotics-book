# Python Agents with `rclpy`

`rclpy` is the Python client library for ROS 2, allowing you to write ROS 2 nodes and interact with the ROS 2 ecosystem using Python. This section will provide examples of creating simple ROS 2 publishers and subscribers.

## Setting up a ROS 2 Workspace

Before you start, ensure you have a ROS 2 workspace. If not, you can create one:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
vcs import src --scm-version Foxy --input https://raw.githubusercontent.com/ros2/ros2/foxy/ros2.repos
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
source install/setup.bash
```

## Creating a Simple Publisher Node

This example demonstrates how to create a ROS 2 node that publishes a string message to a topic.

### `simple_publisher.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):

    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    simple_publisher = SimplePublisher()

    rclpy.spin(simple_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating a Simple Subscriber Node

This example shows how to create a ROS 2 node that subscribes to a topic and receives string messages.

### `simple_subscriber.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    simple_subscriber = SimpleSubscriber()

    rclpy.spin(simple_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    simple_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run these examples:

1.  Save the code in your ROS 2 package.
2.  Build your package (`colcon build`).
3.  Source your workspace (`source install/setup.bash`).
4.  Run the publisher: `ros2 run your_package_name simple_publisher`
5.  Run the subscriber in a new terminal: `ros2 run your_package_name simple_subscriber`

These examples provide a basic foundation for building more complex ROS 2 applications with Python and `rclpy`.
