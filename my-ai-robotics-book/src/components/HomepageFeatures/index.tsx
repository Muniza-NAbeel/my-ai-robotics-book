import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useBaseUrl from "@docusaurus/useBaseUrl";
import styles from "../../pages/index.module.css";
import { useAuth } from "../Auth/AuthProvider";

// ---------- HERO SECTION ----------
function HomepageHeader() {
  const { isAuthenticated } = useAuth();

  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">Physical AI & Humanoid Robotics</h1>
        <p className="hero__subtitle">
          A comprehensive guide to building embodied AI systems using ROS 2,
        </p>
        <div className={styles.heroButtons}>
          <Link
            className={`${styles.heroBtn} button button--secondary button--lg`}
            to={isAuthenticated ? "/docs/intro-foundations/intro" : "/signup"}
          >
            {isAuthenticated ? "Start Reading" : "Get Started"}
          </Link>
        </div>
      </div>
    </header>
  );
}

// ---------- FEATURES (CARDS) ----------
function HomepageFeatures() {
  const { isAuthenticated } = useAuth();

  const chapters = [
    {
      title: "Chapter 1: Introduction Foundations",
      description:
        "Explore the core concepts of physical AI and humanoid robotics.",
      link: "/docs/intro-foundations/intro",
      icon: "🧠",
    },
    {
      title: "Chapter 2: ROS 2 for Robotics",
      description: "Learn how to use ROS 2 to build robust robotic applications.",
      link: "/docs/chapter1-ros2/intro",
      icon: "🤖",
    },
    {
      title: "Chapter 3: Digital Twin & Simulation",
      description:
        "Dive into digital twin technology and robot simulation environments.",
      link: "/docs/chapter2-digital-twin/intro",
      icon: "🛰️",
    },
    {
      title: "Chapter 4: Advanced AI-Robot Perception",
      description:
        "Enhance robot perception with NVIDIA Isaac for AI-driven simulation, ROS, and navigation.",
      link: "/docs/chapter3-ai-robot-brain/intro",
      icon: "⚙️",
    },
    {
      title: "Chapter 5: Vision-Language-Action Integration in Robot Simulations",
      description:
        "Learn to simulate, control, and perceive robots using Gazebo and NVIDIA Isaac for AI-driven robotics..",
      link: "/docs/chapter4-vla/intro",
      icon: "💻",
    },
  ];

  return (
    <section className={styles.features}>
      <div className={styles.grid}>
        {chapters.map((chapter, idx) => (
          <div key={idx} className={styles.card}>
            <div className={styles.cardIcon}>{chapter.icon}</div>
            <h3>{chapter.title}</h3>
            <p>{chapter.description}</p>
            <Link
              className="button button--primary button--md"
              to={isAuthenticated ? chapter.link : "/signup"}
            >
              Read →
            </Link>
          </div>
        ))}
      </div>
    </section>
  );
}

// ---------- MAIN EXPORT ----------
export default function HomepageFeatureSection() {
  return (
    <>
      <HomepageHeader />
      <HomepageFeatures />
    </>
  );
}
