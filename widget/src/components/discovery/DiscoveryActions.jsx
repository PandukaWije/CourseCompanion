import React from "react";
import DiscoveryActionCard from "./DiscoveryActionCard";

const DiscoveryActions = ({ onBrowseCourses, onHelpMeDecide }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <DiscoveryActionCard
        title="I Know What I Want"
        buttonLabel="Browse Course"
        onClick={onBrowseCourses}
      />

      <DiscoveryActionCard
        title="Help Me Decide"
        buttonLabel="Start Discovery"
        onClick={onHelpMeDecide}
      />

      {/* <DiscoveryActionCard
        title="Pick the current course"
        buttonLabel="Start Discovery"
        onClick={() => {
          console.log("Start Discovery clicked");
        }}
      /> */}
    </div>
  );
};

export default DiscoveryActions;
