/**
 * Mock Data for Course Companion Widget
 * Course Discovery Section
 */

export const COURSES = [
  {
    id: "cpp-fundamentals-101",
    title: "C++ Fundamentals",
    description: "Complete C++ programming course from basics to advanced concepts",
    category: "Programming",
    difficulty: "Beginner",
    duration: "6 hours",
    tags: ["programming", "cpp", "beginner", "oop"],
    isPurchased: true
  },
  {
    id: "python-data-science-201",
    title: "Python for Data Science",
    description: "Master Python libraries for data analysis: NumPy, Pandas, Matplotlib",
    category: "Data Science",
    difficulty: "Intermediate",
    duration: "10 hours",
    tags: ["python", "data science", "pandas", "numpy"],
    isPurchased: true
  },
  {
    id: "ml-fundamentals-401",
    title: "Machine Learning Fundamentals",
    description: "Learn supervised and unsupervised learning, neural networks, and deep learning",
    category: "Artificial Intelligence",
    difficulty: "Advanced",
    duration: "14 hours",
    tags: ["machine learning", "ai", "neural networks", "deep learning"],
    isPurchased: false
  },
  {
    id: "web-dev-fullstack-301",
    title: "Full Stack Web Development",
    description: "Build modern web applications with React, Node.js, Express, and MongoDB",
    category: "Web Development",
    difficulty: "Advanced",
    duration: "16 hours",
    tags: ["react", "nodejs", "mongodb", "full stack"],
    isPurchased: true
  },
  {
    id: "dsa-interview-prep-501",
    title: "Data Structures & Algorithms",
    description: "Master DSA for coding interviews at top tech companies",
    category: "Computer Science",
    difficulty: "Intermediate",
    duration: "12 hours",
    tags: ["dsa", "algorithms", "interview", "leetcode"],
    isPurchased: false
  },
  {
    id: "ui-ux-design-101",
    title: "UI/UX Design Principles",
    description: "Create beautiful and intuitive user interfaces with Figma",
    category: "Design",
    difficulty: "Beginner",
    duration: "8 hours",
    tags: ["design", "figma", "ui", "ux"],
    isPurchased: true
  },
  {
    id: "mobile-dev-flutter-601",
    title: "Mobile App Development with Flutter",
    description: "Build cross-platform mobile apps for iOS and Android",
    category: "Mobile Development",
    difficulty: "Intermediate",
    duration: "11 hours",
    tags: ["flutter", "dart", "mobile", "app development"],
    isPurchased: false
  },
  {
    id: "cloud-aws-basics-701",
    title: "AWS Cloud Computing Essentials",
    description: "Learn cloud computing fundamentals with Amazon Web Services",
    category: "Cloud Computing",
    difficulty: "Beginner",
    duration: "9 hours",
    tags: ["aws", "cloud", "devops", "infrastructure"],
    isPurchased: true
  },
  {
    id: "nlp-transformers-801",
    title: "NLP with Transformers",
    description: "Build state-of-the-art NLP models with transformers and BERT",
    category: "Artificial Intelligence",
    difficulty: "Advanced",
    duration: "13 hours",
    tags: ["nlp", "transformers", "bert", "ai"],
    isPurchased: false
  },
  {
    id: "cybersecurity-basics-901",
    title: "Cybersecurity Fundamentals",
    description: "Learn essential cybersecurity concepts and defense strategies",
    category: "Cybersecurity",
    difficulty: "Beginner",
    duration: "7 hours",
    tags: ["security", "cybersecurity", "hacking", "network"],
    isPurchased: true
  }
];

export const CATEGORIES = [
  { id: "all", name: "All" },
  { id: "programming", name: "Programming" },
  { id: "data-science", name: "Data Science" },
  { id: "web-development", name: "Web Dev" },
  { id: "ai", name: "AI/ML" },
  { id: "design", name: "Design" },
  { id: "mobile", name: "Mobile" },
  { id: "cloud", name: "Cloud" },
  { id: "security", name: "Security" }
];

// Discovery Agent Conversation Logic
export class DiscoveryAgent {
  constructor() {
    this.state = "initial";
    this.context = {
      interest: null,
      experience: null,
      goal: null
    };
  }

  getInitialMessage() {
    return {
      type: "assistant",
      content: "Hi! I'm here to help you find the perfect course. What would you like to learn today?"
    };
  }

  processMessage(userMessage) {
    const messageLower = userMessage.toLowerCase();

    // Handle greetings
    if (this.isGreeting(messageLower)) {
      return {
        type: "assistant",
        content: "Hello! Great to meet you! Tell me, what area are you interested in exploring? Programming, Data Science, Web Development, or something else?"
      };
    }

    // State-based responses
    switch (this.state) {
      case "initial":
        return this.handleInitialState(messageLower);
      case "experience":
        return this.handleExperienceState(messageLower);
      case "goal":
        return this.handleGoalState(messageLower);
      default:
        return this.handleInitialState(messageLower);
    }
  }

  isGreeting(message) {
    const greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"];
    return greetings.some(g => message.includes(g));
  }

  handleInitialState(message) {
    // Detect interest
    const interests = {
      "programming": ["programming", "code", "coding", "c++", "python", "java"],
      "data science": ["data", "analytics", "pandas", "numpy"],
      "web": ["web", "website", "frontend", "backend", "react"],
      "machine learning": ["machine learning", "ml", "ai", "neural"],
      "mobile": ["mobile", "app", "flutter", "ios", "android"],
      "design": ["design", "ui", "ux", "figma"],
      "cloud": ["cloud", "aws", "azure", "devops"],
      "security": ["security", "cybersecurity", "hacking"]
    };

    for (const [interest, keywords] of Object.entries(interests)) {
      if (keywords.some(k => message.includes(k))) {
        this.context.interest = interest;
        this.state = "experience";
        return {
          type: "assistant",
          content: `Great choice! ${interest.charAt(0).toUpperCase() + interest.slice(1)} is a fantastic field. What's your experience level?`,
          options: [
            { label: "Complete Beginner", value: "beginner" },
            { label: "Some Experience", value: "intermediate" },
            { label: "Advanced", value: "advanced" }
          ]
        };
      }
    }

    return {
      type: "assistant",
      content: "That sounds interesting! Could you tell me more? Are you interested in programming, data science, web development, or something else?"
    };
  }

  handleExperienceState(message) {
    if (message.includes("beginner") || message.includes("new") || message.includes("starting")) {
      this.context.experience = "beginner";
    } else if (message.includes("intermediate") || message.includes("some")) {
      this.context.experience = "intermediate";
    } else if (message.includes("advanced") || message.includes("expert")) {
      this.context.experience = "advanced";
    }

    this.state = "goal";
    return {
      type: "assistant",
      content: "Perfect! What's your main goal?",
      options: [
        { label: "Career Change", value: "career" },
        { label: "Skill Enhancement", value: "skill" },
        { label: "Personal Project", value: "project" },
        { label: "Interview Prep", value: "interview" }
      ]
    };
  }

  handleGoalState(message) {
    if (message.includes("career")) {
      this.context.goal = "career";
    } else if (message.includes("skill") || message.includes("enhance")) {
      this.context.goal = "skill";
    } else if (message.includes("project")) {
      this.context.goal = "project";
    } else if (message.includes("interview")) {
      this.context.goal = "interview";
    }

    // Generate recommendations
    const recommendations = this.getRecommendations();
    this.state = "completed";

    return {
      type: "courses",
      content: "Based on your interests and goals, I recommend these courses:",
      courses: recommendations
    };
  }

  getRecommendations() {
    const { interest, experience } = this.context;
    
    // Map interests and experience to courses
    const mapping = {
      "programming": {
        "beginner": ["cpp-fundamentals-101", "ui-ux-design-101"],
        "intermediate": ["dsa-interview-prep-501", "web-dev-fullstack-301"],
        "advanced": ["ml-fundamentals-401", "nlp-transformers-801"]
      },
      "data science": {
        "beginner": ["python-data-science-201"],
        "intermediate": ["python-data-science-201", "ml-fundamentals-401"],
        "advanced": ["ml-fundamentals-401", "nlp-transformers-801"]
      },
      "web": {
        "beginner": ["ui-ux-design-101"],
        "intermediate": ["web-dev-fullstack-301"],
        "advanced": ["web-dev-fullstack-301"]
      },
      "machine learning": {
        "beginner": ["python-data-science-201"],
        "intermediate": ["ml-fundamentals-401"],
        "advanced": ["ml-fundamentals-401", "nlp-transformers-801"]
      },
      "mobile": ["mobile-dev-flutter-601"],
      "design": ["ui-ux-design-101"],
      "cloud": ["cloud-aws-basics-701"],
      "security": ["cybersecurity-basics-901"]
    };

    let courseIds = [];
    if (mapping[interest]) {
      if (typeof mapping[interest] === "object" && !Array.isArray(mapping[interest])) {
        courseIds = mapping[interest][experience] || mapping[interest]["beginner"];
      } else {
        courseIds = mapping[interest];
      }
    }

    // Fallback
    if (courseIds.length === 0) {
      courseIds = ["cpp-fundamentals-101", "ui-ux-design-101"];
    }

    // Get course objects and add match scores
    const courses = courseIds.map((id, index) => {
      const course = COURSES.find(c => c.id === id);
      return {
        ...course,
        match: `${95 - index * 5}% match`
      };
    });

    return courses.slice(0, 3); // Return top 3
  }

  reset() {
    this.state = "initial";
    this.context = {
      interest: null,
      experience: null,
      goal: null
    };
  }
}

// Helper functions
export const searchCourses = (query) => {
  if (!query) return COURSES;
  
  const queryLower = query.toLowerCase();
  return COURSES.filter(course =>
    course.title.toLowerCase().includes(queryLower) ||
    course.description.toLowerCase().includes(queryLower) ||
    course.tags.some(tag => tag.toLowerCase().includes(queryLower))
  );
};

export const filterByCategory = (category) => {
  if (category === "all") return COURSES;
  
  return COURSES.filter(course =>
    course.category.toLowerCase().includes(category.toLowerCase())
  );
};

export const getCourseById = (id) => {
  return COURSES.find(course => course.id === id);
};

// Get only purchased courses (for "I Know What I Want")
export const getPurchasedCourses = () => {
  return COURSES.filter(course => course.isPurchased);
};