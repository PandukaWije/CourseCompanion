import React, { useState } from "react";
import { DiscoveryHeader } from "./DiscoveryHeader";
import DiscoveryPage from "./DiscoveryPage";
import KnowWhatIWantPage from "./KnowWhatIWantPage";
import HelpMeDecidePage from "./HelpMeDecidePage";
import { X, ArrowRight } from 'lucide-react';
import { useWidgetStore } from "../../store/widgetStore";

/**
 * DiscoveryPageLayout Component
 * Header + Main Content Area + Selected Courses Bar
 */
export const DiscoveryPageLayout = () => {
  const [view, setView] = useState("MAIN");
  const { selectedCourses, removeCourse, clearCourses, setView: setWidgetView, openPanel} = useWidgetStore();

  // Handle proceed to chat
  const handleProceed = () => {
    if (selectedCourses.length > 0) {
      // Navigate to chat view
      openPanel('chat');
    }
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Header */}
      <DiscoveryHeader />

      {/* Main Content Area - with bottom padding for selection bar */}
      <div className={`flex-1 overflow-y-auto ${selectedCourses.length > 0 ? 'pb-32' : ''}`}>
        {view === "MAIN" && (
          <DiscoveryPage 
            onBrowseCourses={() => setView("KNOW")}
            onHelpMeDecide={() => setView("HELP")}
          />
        )}

        {view === "KNOW" && (
          <KnowWhatIWantPage onBack={() => setView("MAIN")}/>
        )}

        {view === "HELP" && (
          <HelpMeDecidePage onBack={() => setView("MAIN")}/>
        )}
      </div>

      {/* Selected Courses Bar - Positioned at bottom of widget panel */}
      {selectedCourses.length > 0 && (
        <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg p-4 z-10">
          {/* Selected Courses */}
          <div className="flex items-center gap-3 mb-3">
            <div className="flex-1 flex items-center gap-2 overflow-x-auto">
              <span className="text-sm font-medium text-gray-700 whitespace-nowrap">
                Selected ({selectedCourses.length}):
              </span>
              <div className="flex gap-2">
                {selectedCourses.map((course) => (
                  <div
                    key={course.id}
                    className="flex items-center gap-2 px-3 py-1.5 bg-violet-50 
                             border border-violet-200 rounded-lg whitespace-nowrap"
                  >
                    <span className="text-sm text-gray-900 max-w-[150px] truncate">
                      {course.title}
                    </span>
                    <button
                      onClick={() => removeCourse(course.id)}
                      className="ml-1 text-gray-400 hover:text-gray-600"
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Clear All */}
            {selectedCourses.length > 1 && (
              <button
                onClick={clearCourses}
                className="text-sm text-gray-500 hover:text-gray-700 whitespace-nowrap"
              >
                Clear all
              </button>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleProceed}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 
                       bg-gradient-to-r from-violet-500 to-purple-600 text-white 
                       rounded-lg font-medium hover:shadow-lg transition"
            >
              <span>Proceed to Chat</span>
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DiscoveryPageLayout;