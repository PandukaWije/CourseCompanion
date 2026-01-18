import React, { useState, useRef, useEffect } from "react";
import { ArrowLeft, Sparkles, Send, Check, ShoppingCart } from "lucide-react";
import { DiscoveryAgent } from "../../data/mockdata";
import { useWidgetStore } from "../../store/widgetStore";

const HelpMeDecidePage = ({ onBack }) => {
  const [agent] = useState(() => new DiscoveryAgent());
  const [messages, setMessages] = useState([agent.getInitialMessage()]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  
  const { selectedCourses, addCourse, removeCourse } = useWidgetStore();

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Check if course is selected
  const isSelected = (courseId) => {
    return selectedCourses.some(c => c.id === courseId);
  };

  // Handle course selection (only for purchased courses)
  const handleCourseClick = (course) => {
    if (!course.isPurchased) return; // Don't allow selection of unpurchased courses
    
    if (isSelected(course.id)) {
      removeCourse(course.id);
    } else {
      addCourse(course);
    }
  };

  // Handle purchase button click
  const handlePurchase = (course) => {
    // This will be connected to your purchase flow
    console.log("Purchase course:", course.id);
    // You can trigger a modal or redirect to purchase page here
  };

  // Handle send message
  const handleSendMessage = (messageText = inputValue) => {
    if (!messageText.trim()) return;

    // Add user message
    const userMessage = {
      type: "user",
      content: messageText
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);

    // Simulate bot thinking delay
    setTimeout(() => {
      const response = agent.processMessage(messageText);
      setMessages(prev => [...prev, response]);
      setIsTyping(false);
    }, 800);
  };

  // Handle option click
  const handleOptionClick = (option) => {
    handleSendMessage(option.label || option.value);
  };

  return (
    <div className="w-full px-6 pt-6 pb-3 flex flex-col h-full">
      <div className="mx-auto flex flex-col h-full w-full space-y-4">
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
          Help me decide
        </h1>

        {/* Chat Messages Container - Add padding at bottom when courses selected */}
        <div className={`flex-1 space-y-4 overflow-y-auto ${selectedCourses.length > 0 ? 'pb-4' : ''}`}>
          {messages.map((message, index) => (
            <div key={index}>
              {message.type === "courses" ? (
                // Recommended Courses
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center flex-shrink-0">
                    <Sparkles size={16} className="text-violet-600" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm bg-gray-100 rounded-lg p-3 text-gray-900 mb-3">
                      {message.content}
                    </p>
                    <div className="space-y-2">
                      {message.courses && message.courses.map((course) => (
                        <div
                          key={course.id}
                          className={`w-full text-left p-3 rounded-lg border transition ${
                            course.isPurchased
                              ? isSelected(course.id)
                                ? "border-violet-500 bg-violet-50"
                                : "border-gray-200 hover:border-violet-300 hover:bg-gray-50 cursor-pointer"
                              : "border-gray-200 bg-gray-50 cursor-default"
                          }`}
                        >
                          <div className="flex gap-3">
                            {/* Course Info */}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-start justify-between gap-2">
                                <div className="flex-1" onClick={() => course.isPurchased && handleCourseClick(course)}>
                                  <h4 className="font-semibold text-gray-900 text-sm">
                                    {course.title}
                                  </h4>
                                  <p className="text-xs text-gray-500 mt-1">
                                    {course.description}
                                  </p>
                                </div>
                                
                                {/* Match Score & Action */}
                                <div className="flex items-center gap-2 flex-shrink-0">
                                  <span className="text-xs font-medium text-violet-600 bg-violet-50 px-2 py-1 rounded whitespace-nowrap">
                                    {course.match}
                                  </span>
                                  
                                  {course.isPurchased ? (
                                    // Selection checkbox for purchased courses
                                    <button
                                      onClick={() => handleCourseClick(course)}
                                      className={`w-6 h-6 rounded-full flex items-center justify-center ${
                                        isSelected(course.id)
                                          ? "bg-violet-500"
                                          : "border-2 border-gray-300 hover:border-violet-400"
                                      }`}
                                    >
                                      {isSelected(course.id) && (
                                        <Check size={12} className="text-white" />
                                      )}
                                    </button>
                                  ) : (
                                    // Purchase button for unpurchased courses
                                    <button
                                      onClick={() => handlePurchase(course)}
                                      className="flex items-center gap-1 px-2 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-xs font-medium transition"
                                    >
                                      <ShoppingCart size={12} />
                                      Purchase
                                    </button>
                                  )}
                                </div>
                              </div>
                              
                              {/* Course Meta */}
                              <div className="flex items-center gap-2 mt-2 text-xs">
                                <span className={`px-1.5 py-0.5 rounded ${
                                  course.difficulty === "Beginner"
                                    ? "bg-green-100 text-green-700"
                                    : course.difficulty === "Intermediate"
                                    ? "bg-blue-100 text-blue-700"
                                    : "bg-purple-100 text-purple-700"
                                }`}>
                                  {course.difficulty}
                                </span>
                                <span className="text-gray-500">{course.duration}</span>
                                {!course.isPurchased && (
                                  <span className="px-1.5 py-0.5 rounded bg-amber-100 text-amber-700">
                                    Not Enrolled
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                // Regular Message
                <div
                  className={`flex gap-3 ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.type === "assistant" && (
                    <div className="w-8 h-8 rounded-full bg-[var(--cc-secondary-bg)] flex items-center justify-center flex-shrink-0">
                      <Sparkles size={16} className="text-violet-600" />
                    </div>
                  )}
                  
                  <div className={`flex-1 ${message.type === "user" ? "max-w-xs ml-auto" : "max-w-md"}`}>
                    <p
                      className={`text-sm rounded-lg p-3 ${
                        message.type === "user"
                          ? "bg-violet-500 text-white"
                          : "bg-gray-100 text-gray-900"
                      }`}
                    >
                      {message.content}
                    </p>
                    
                    {/* Options */}
                    {message.options && (
                      <div className="mt-3 space-y-2">
                        {message.options.map((option, i) => (
                          <button
                            key={i}
                            onClick={() => handleOptionClick(option)}
                            className="w-full text-left p-3 rounded-lg border border-gray-200 
                                     hover:border-violet-300 hover:bg-violet-50 transition"
                          >
                            <span className="font-medium text-gray-900 text-sm">
                              {option.label}
                            </span>
                          </button>
                        ))}
                      </div>
                    )}
                    
                    <span className="text-xs text-gray-500 mt-1 block">
                      {message.type === "user" ? "You" : "AI Assistant"}
                    </span>
                  </div>
                </div>
              )}
            </div>
          ))}
          
          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center flex-shrink-0">
                <Sparkles size={16} className="text-violet-600" />
              </div>
              <div className="flex items-center p-3 bg-gray-100 rounded-lg">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Box - Fixed position, not affected by bottom bar */}
        <div className="flex gap-2 border-t border-gray-200 pt-4 bg-white">
          <input
            type="text"
            placeholder="Type your message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            className="flex-1 pl-4 pr-4 py-2 rounded-lg border border-gray-300
                       focus:outline-none focus:ring-2 focus:ring-violet-400
                       text-gray-900 bg-white"
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!inputValue.trim() || isTyping}
            className="p-2 rounded-lg bg-violet-500 text-white hover:bg-violet-600 
                       disabled:bg-gray-300 transition flex-shrink-0"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default HelpMeDecidePage;