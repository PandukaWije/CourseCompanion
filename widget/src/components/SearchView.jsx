import React, { useState } from 'react';
import { Search, Filter, Clock, Star } from 'lucide-react';

/**
 * SearchView Component
 * Placeholder for the Course Search interface
 */
const SearchView = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const mockCourses = [
    {
      id: 1,
      title: 'Introduction to Machine Learning',
      category: 'AI & ML',
      duration: '8 weeks',
      rating: 4.8,
      students: 1234,
    },
    {
      id: 2,
      title: 'Web Development Bootcamp',
      category: 'Programming',
      duration: '12 weeks',
      rating: 4.9,
      students: 2341,
    },
    {
      id: 3,
      title: 'Data Science Fundamentals',
      category: 'Data Science',
      duration: '10 weeks',
      rating: 4.7,
      students: 987,
    },
  ];

  return (
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-purple focus:border-transparent"
          placeholder="Search courses..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-2">
        <button className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </button>
        <button className="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
          All Categories
        </button>
      </div>

      {/* Results */}
      <div className="space-y-3">
        <p className="text-sm text-gray-600">
          Showing {mockCourses.length} courses
        </p>

        {mockCourses.map((course) => (
          <div
            key={course.id}
            className="p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer"
          >
            <h3 className="text-base font-semibold text-gray-900 mb-2">
              {course.title}
            </h3>
            
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span className="inline-flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {course.duration}
              </span>
              <span className="inline-flex items-center">
                <Star className="w-4 h-4 mr-1 text-yellow-400 fill-current" />
                {course.rating}
              </span>
            </div>

            <div className="mt-3 flex items-center justify-between">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-brand-purple">
                {course.category}
              </span>
              <span className="text-xs text-gray-500">
                {course.students.toLocaleString()} students
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Load More */}
      <button className="w-full py-3 text-sm font-medium text-brand-purple hover:text-brand-pink transition-colors">
        Load more courses
      </button>
    </div>
  );
};

export default SearchView;