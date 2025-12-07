import React from "react";
import Layout from "@theme/Layout";
import HomepageFeatureSection from "../components/HomepageFeatures";
import Chatbot from "../components/Chatbot";

export default function Home() {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="Build intelligent robots"
    >
      <Chatbot />
      <HomepageFeatureSection />
    </Layout>
  );
}
