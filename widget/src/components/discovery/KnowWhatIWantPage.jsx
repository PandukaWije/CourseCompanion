import React, { useState } from "react";
import { ArrowLeft, Search, Check } from "lucide-react";
import { getPurchasedCourses, CATEGORIES, searchCourses, filterByCategory } from "../../data/mockdata";
import { useWidgetStore } from "../../store/widgetStore";

const KnowWhatIWantPage = ({ onBack }) => {
  const [query, setQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [filteredCourses, setFilteredCourses] = useState(getPurchasedCourses());
  
  const { selectedCourses, addCourse, removeCourse } = useWidgetStore();

  // Handle search - only in purchased courses
  const handleSearch = (searchQuery) => {
    setQuery(searchQuery);
    let purchasedCourses = getPurchasedCourses();
    let results = searchQuery 
      ? purchasedCourses.filter(course =>
          course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          course.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
          course.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
        )
      : purchasedCourses;
    
    if (selectedCategory !== "all") {
      results = results.filter(course =>
        course.category.toLowerCase().includes(selectedCategory.toLowerCase())
      );
    }
    
    setFilteredCourses(results);
  };

  // Handle category filter - only in purchased courses
  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    let purchasedCourses = getPurchasedCourses();
    let results = category === "all" 
      ? purchasedCourses 
      : purchasedCourses.filter(course =>
          course.category.toLowerCase().includes(category.toLowerCase())
        );
    
    if (query) {
      results = results.filter(course =>
        course.title.toLowerCase().includes(query.toLowerCase()) ||
        course.description.toLowerCase().includes(query.toLowerCase())
      );
    }
    
    setFilteredCourses(results);
  };

  // Check if course is selected
  const isSelected = (courseId) => {
    return selectedCourses.some(c => c.id === courseId);
  };

  // Handle course selection
  const handleCourseClick = (course) => {
    if (isSelected(course.id)) {
      removeCourse(course.id);
    } else {
      addCourse(course);
    }
  };

  return (
    <div className="w-full px-6 py-6">
      <div className="mx-auto space-y-6">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft size={16} />
          Back to discovery
        </button>

        {/* Title */}
        <h1 className="text-xl font-semibold text-gray-900">
          Browse your Courses
        </h1>

        {/* Search Bar */}
        <div className="relative">
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          />
          <input
            type="text"
            placeholder="Search your courses..."
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-300 
                       focus:outline-none focus:ring-2 focus:ring-violet-400
                       text-gray-900 bg-white"
          />
        </div>

        {/* Category Filter */}
        <div className="flex gap-2 overflow-x-auto pb-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => handleCategoryChange(cat.id)}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition ${
                selectedCategory === cat.id
                  ? "bg-violet-500 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>

        {/* Course List - REMOVED max-h and overflow-y-auto to fix double scrolling */}
        <div className="space-y-3">
          {filteredCourses.length > 0 ? (
            filteredCourses.map((course) => (
              <button
                key={course.id}
                className={`w-full text-left p-4 rounded-xl border transition ${
                  isSelected(course.id)
                    ? "border-violet-500 bg-violet-50"
                    : "border-gray-200 hover:border-violet-300 hover:bg-gray-50"
                }`}
                onClick={() => handleCourseClick(course)}
              >
                <div className="flex items-start justify-between gap-3">
                  {/* Course Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 text-base">
                          {course.title}
                        </h3>
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                          {course.description}
                        </p>
                      </div>
                      
                      {/* Selection Indicator */}
                      {isSelected(course.id) && (
                        <div className="w-6 h-6 rounded-full bg-violet-500 flex items-center justify-center flex-shrink-0">
                          <Check size={14} className="text-white" />
                        </div>
                      )}
                    </div>
                    
                    {/* Course Meta */}
                    <div className="flex items-center gap-3 mt-2 text-xs">
                      <span className={`px-2 py-0.5 rounded ${
                        course.difficulty === "Beginner"
                          ? "bg-green-100 text-green-700"
                          : course.difficulty === "Intermediate"
                          ? "bg-blue-100 text-blue-700"
                          : "bg-purple-100 text-purple-700"
                      }`}>
                        {course.difficulty}
                      </span>
                      <span className="text-gray-500">{course.duration}</span>
                    </div>
                  </div>
                </div>
              </button>
            ))
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No courses found</p>
              <p className="text-sm text-gray-400 mt-1">Try adjusting your search or filters</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowWhatIWantPage;