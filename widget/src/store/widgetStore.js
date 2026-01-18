import { create } from 'zustand';

/**
 * CourseCompanion Widget Store - Updated with Chat Course Context
 * Manages the global state of the widget including immutable course context for chats
 */
export const useWidgetStore = create((set, get) => ({
  // ============================================
  // Widget State
  // ============================================
  
  // Widget visibility states
  isButtonVisible: true,
  isMenuOpen: false,
  isPanelOpen: false,
  
  // Current view in the panel
  currentView: null, // null | 'discovery' | 'search' | 'chat'
  
  // Active menu icon
  activeIcon: null,
  
  // ============================================
  // Configuration
  // ============================================
  
  config: {
    userId: null,
    apiUrl: 'http://localhost:8000',
    theme: 'light',
    position: 'bottom-right',
  },
  
  // ============================================
  // User State
  // ============================================
  
  userId: null,
  selectedCourse: null,
  selectedCourses: [], // Array of { id, name } objects
  
  // ============================================
  // Chat State with Immutable Course Context
  // ============================================
  
  currentChatId: null,
  chats: [], // Array of chat objects with immutable courseContext
  messages: [], // Messages for current chat
  
  // ============================================
  // Actions
  // ============================================
  
  /**
   * Initialize widget with configuration
   */
  initWidget: (config) => set((state) => ({
    config: { ...state.config, ...config },
    userId: config.userId || null,
  })),
  
  /**
   * Toggle floating button visibility
   */
  toggleButton: () => set((state) => ({
    isButtonVisible: !state.isButtonVisible,
  })),
  
  /**
   * Open the floating menu
   */
  openMenu: () => set({
    isMenuOpen: true,
  }),
  
  /**
   * Close the floating menu
   */
  closeMenu: () => set({
    isMenuOpen: false,
    activeIcon: null,
  }),
  
  /**
   * Toggle menu open/close
   */
  toggleMenu: () => set((state) => ({
    isMenuOpen: !state.isMenuOpen,
    isPanelOpen: state.isMenuOpen ? false : state.isPanelOpen,
    currentView: state.isMenuOpen ? null : state.currentView,
    activeIcon: state.isMenuOpen ? null : state.activeIcon,
  })),
  
  /**
   * Set active icon in menu
   */
  setActiveIcon: (icon) => set({
    activeIcon: icon,
  }),
  
  /**
   * Open a specific panel view
   */
  openPanel: (view) => set({
    isPanelOpen: true,
    currentView: view,
    activeIcon: view,
  }),
  
  /**
   * Close the panel
   */
  closePanel: () => set({
    isPanelOpen: false,
    currentView: null,
    activeIcon: null,
  }),
  
  /**
   * Toggle panel open/close
   */
  togglePanel: () => set((state) => ({
    isPanelOpen: !state.isPanelOpen,
    currentView: state.isPanelOpen ? null : state.currentView,
  })),
  
  /**
   * Set current view
   */
  setView: (view) => set({
    currentView: view,
    isPanelOpen: true,
  }),
  
  /**
   * Set selected course
   */
  setSelectedCourse: (course) => set({
    selectedCourse: course,
  }),
  
  /**
   * Add course to selection
   */
  addCourse: (course) => set((state) => {
    if (state.selectedCourses.some(c => c.id === course.id)) {
      return state;
    }
    return {
      selectedCourses: [...state.selectedCourses, course]
    };
  }),
  
  /**
   * Remove course from selection
   */
  removeCourse: (courseId) => set((state) => ({
    selectedCourses: state.selectedCourses.filter(c => c.id !== courseId)
  })),
  
  /**
   * Clear all selected courses
   */
  clearCourses: () => set({
    selectedCourses: []
  }),
  
  /**
   * Set selected courses (replaces entire array)
   */
  setSelectedCourses: (courses) => set({
    selectedCourses: courses
  }),
  
  // ============================================
  // Chat Management with Immutable Course Context
  // ============================================
  
  /**
   * Create a new chat with immutable course context
   */
  createNewChat: (title = 'New Chat') => {
    const state = get();
    const newChat = {
      chatId: `chat_${Date.now()}`,
      title,
      courseContext: [...state.selectedCourses], // Immutable snapshot of courses
      messages: [],
      messageCount: 0,
      createdAt: new Date(),
      lastActivity: new Date(),
    };
    
    set({
      chats: [newChat, ...state.chats],
      currentChatId: newChat.chatId,
      messages: [],
    });
    
    return newChat.chatId;
  },
  
  /**
   * Open an existing chat
   * If courseContext provided, switch to those courses
   */
  openChat: (chatId, switchToCourses = false) => {
    const state = get();
    const chat = state.chats.find(c => c.chatId === chatId);
    
    if (!chat) {
      console.error('Chat not found:', chatId);
      return;
    }
    
    const updates = {
      currentChatId: chatId,
      messages: chat.messages || [],
    };
    
    // If requested, switch to the chat's original courses
    if (switchToCourses) {
      updates.selectedCourses = [...chat.courseContext];
    }
    
    set(updates);
  },
  
  /**
   * Add message to current chat
   */
  addMessage: (message) => set((state) => {
    const newMessage = {
      id: `msg_${Date.now()}`,
      ...message,
      timestamp: new Date(),
    };
    
    // Update messages
    const updatedMessages = [...state.messages, newMessage];
    
    // Update chat in chats array
    const updatedChats = state.chats.map(chat => {
      if (chat.chatId === state.currentChatId) {
        return {
          ...chat,
          messages: updatedMessages,
          messageCount: updatedMessages.length,
          lastActivity: new Date(),
          lastMessage: message.content,
        };
      }
      return chat;
    });
    
    return {
      messages: updatedMessages,
      chats: updatedChats,
    };
  }),
  
  /**
   * Update chat title
   */
  updateChatTitle: (chatId, title) => set((state) => ({
    chats: state.chats.map(chat =>
      chat.chatId === chatId ? { ...chat, title } : chat
    )
  })),
  
  /**
   * Delete a chat
   */
  deleteChat: (chatId) => set((state) => {
    const updatedChats = state.chats.filter(c => c.chatId !== chatId);
    
    return {
      chats: updatedChats,
      currentChatId: state.currentChatId === chatId ? null : state.currentChatId,
      messages: state.currentChatId === chatId ? [] : state.messages,
    };
  }),
  
  /**
   * Get chats filtered by course context
   */
  getChatsForCourses: (courseIds, matchType = 'any') => {
    const state = get();
    
    if (matchType === 'exact') {
      // Exact match: chat must have exactly these courses
      return state.chats.filter(chat => {
        const chatCourseIds = chat.courseContext.map(c => c.id).sort();
        const targetIds = [...courseIds].sort();
        
        return chatCourseIds.length === targetIds.length &&
               chatCourseIds.every((id, index) => id === targetIds[index]);
      });
    } else {
      // Any match: chat must include at least one of these courses
      return state.chats.filter(chat =>
        chat.courseContext.some(course => courseIds.includes(course.id))
      );
    }
  },
  
  /**
   * Check if can proceed to chat
   */
  canProceed: () => {
    const state = get();
    return state.selectedCourses.length > 0;
  },
  
  /**
   * Reset widget to initial state
   */
  resetWidget: () => set({
    isMenuOpen: false,
    isPanelOpen: false,
    currentView: null,
    activeIcon: null,
    selectedCourse: null,
    selectedCourses: [],
    currentChatId: null,
    messages: [],
  }),
}));