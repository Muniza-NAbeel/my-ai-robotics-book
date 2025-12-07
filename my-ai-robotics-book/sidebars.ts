import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  bookSidebar: [
    {
      type: 'category',
      label: 'Introduction and Foundations',
      link: {type: 'doc', id: 'intro-foundations/intro'},
      items: [
        'intro-foundations/physical-ai-basics',
        'intro-foundations/embodied-intelligence',
        'intro-foundations/sensors-overview',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 1: Learning ROS 2 Fundamentals',
      link: {type: 'doc', id: 'chapter1-ros2/intro'},
      items: [
        'chapter1-ros2/nodes-topics-services',
        'chapter1-ros2/python-agents-rclpy',
        'chapter1-ros2/urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: Simulating Digital Twins',
      link: {type: 'doc', id: 'chapter2-digital-twin/intro'},
      items: [
        'chapter2-digital-twin/gazebo-physics',
        'chapter2-digital-twin/unity-rendering',
        'chapter2-digital-twin/sensor-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: Advanced AI-Robot Perception',
      link: {type: 'doc', id: 'chapter3-ai-robot-brain/intro'},
      items: [
        'chapter3-ai-robot-brain/nvidia-isaac-sim',
        'chapter3-ai-robot-brain/isaac-ros',
        'chapter3-ai-robot-brain/nav2-path-planning',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: Vision-Language-Action Integration',
      link: {type: 'doc', id: 'chapter4-vla/intro'},
      items: [
        'chapter4-vla/voice-to-action',
        'chapter4-vla/cognitive-planning',
        'chapter4-vla/capstone-project',
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
