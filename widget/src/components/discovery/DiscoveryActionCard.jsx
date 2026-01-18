import React from "react";

const DiscoveryActionCard = ({ title, buttonLabel, onClick }) => {
  return (
    <div className="border rounded-xl !p-6 flex flex-col justify-between bg-white shadow-sm">
      <h2 className="text-lg font-medium text-gray-900 !mb-4 text-center">
        {title}
      </h2>

      <button
        onClick={onClick}
        className="!mt-auto w-full rounded-full !py-2 text-sm font-medium
                   bg-violet-100 text-violet-700 hover:bg-violet-200 transition"
      >
        {buttonLabel}
      </button>
    </div>
  );
};

export default DiscoveryActionCard;
