import React from "react";
import DiscoveryHero from "./DiscoveryHero";
import DiscoveryActions from "./DiscoveryActions";

const DiscoveryPage = ({ onBrowseCourses, onHelpMeDecide }) => {
  return (
    <div className="w-full px-6 py-6">
      <div className="mx-auto space-y-6">
        <DiscoveryHero />
        <DiscoveryActions
          onBrowseCourses={onBrowseCourses}
          onHelpMeDecide={onHelpMeDecide}
        />
      </div>
    </div>
  );
};

export default DiscoveryPage;
