# 🎓 CourseCompanion Widget

> AI-Powered Learning Assistant Widget - Inject intelligent course discovery and RAG chatbot into any website

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.1-646cff.svg)](https://vitejs.dev/)

---

## 📋 Overview

CourseCompanion Widget is an injectable, self-contained learning assistant that can be embedded into any website with just a few lines of code. It provides:

- **🎯 AI Course Discovery** - Intelligent recommendations based on user goals
- **🔍 Smart Search** - Quick course search with advanced filters
- **💬 RAG Chatbot** - Context-aware assistant with course knowledge
- **📝 Learning Tools** - Notes, mind maps, quizzes, and artifacts

---

## ✨ Features

### 🎨 Beautiful UI
- Gradient design matching modern aesthetics
- Smooth animations and transitions
- Mobile-responsive design
- Shadow DOM for style isolation

### 🚀 Easy Integration
- Single script tag integration
- Zero dependencies on host page
- No CSS conflicts
- Works with any framework

### 🤖 AI-Powered
- LangGraph-based discovery agent
- RAG-powered chatbot
- Personalized recommendations
- Context-aware responses

### 🔒 Secure & Isolated
- Shadow DOM encapsulation
- No global namespace pollution
- Protected from host page styles
- Sandboxed execution

---

## 🎯 Quick Start

### Installation

```bash
# Navigate to widget directory
cd widget

# Install dependencies
npm install

# Start development server
npm run dev
```

The widget will be available at `http://localhost:5173`

### Build for Production

```bash
# Build the widget
npm run build

# Output will be in dist/coursecompanion-widget.iife.js
```

---

## 📦 Integration

### Method 1: Script Tag (Recommended)

Add these lines before the closing `</body>` tag:

```html
<!-- Load the widget -->
<script src="https://your-cdn.com/coursecompanion-widget.js"></script>

<!-- Initialize -->
<script>
  window.CourseCompanion.init({
    userId: "user_12345",
    apiUrl: "https://api.coursecompanion.com",
    theme: "light",
    position: "bottom-right"
  });
</script>
```

### Method 2: npm Package

```bash
npm install coursecompanion-widget
```

```javascript
import CourseCompanion from 'coursecompanion-widget';

CourseCompanion.init({
  userId: "user_12345",
  apiUrl: "https://api.coursecompanion.com"
});
```

---

## ⚙️ Configuration

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `userId` | string | User identifier for personalization | `null` |
| `apiUrl` | string | Backend API endpoint | `http://localhost:8000` |
| `theme` | string | Widget theme (`light` or `dark`) | `light` |
| `position` | string | Screen position | `bottom-right` |

### Example with All Options

```javascript
window.CourseCompanion.init({
  userId: "user_12345",
  apiUrl: "https://api.coursecompanion.com",
  theme: "light",
  position: "bottom-right"
});
```

---

## 🎨 UI Flow

The widget follows a progressive disclosure pattern:

1. **Stage 1**: Circular gradient button (✨)
2. **Stage 2**: Horizontal menu panel (👥 🔍 💬)
3. **Stage 3**: Full panel with selected feature

### Interaction Sequence

```
Floating Button → Menu Panel → Full Panel
     (✨)      →   (👥🔍💬)  →  (Content)
```

---

## 🏗️ Architecture

### Project Structure

```
widget/
├── src/
│   ├── main.jsx                    # Entry point & Shadow DOM injection
│   ├── App.jsx                     # Main orchestrator
│   ├── components/
│   │   ├── FloatingButton.jsx      # Circular button
│   │   ├── FloatingMenuPanel.jsx   # Icon menu
│   │   ├── WidgetPanel.jsx         # Panel container
│   │   ├── DiscoveryView.jsx       # Course discovery
│   │   ├── SearchView.jsx          # Search interface
│   │   └── ChatView.jsx            # Chat interface
│   ├── store/
│   │   └── widgetStore.js          # Zustand state
│   ├── utils/
│   │   └── shadowDom.js            # Shadow DOM utilities
│   └── styles/
│       └── widget.css              # Scoped styles
├── public/
│   └── sample.html                 # Demo page
├── package.json
├── vite.config.js                  # Build config
└── README.md
```

### Technology Stack

- **React 18.3** - UI framework
- **Vite 5.1** - Build tool
- **Zustand** - State management
- **TailwindCSS** - Styling
- **Lucide React** - Icons
- **Shadow DOM** - Style isolation

---

## 🔧 API Methods

### `init(config)`

Initialize the widget with configuration.

```javascript
window.CourseCompanion.init({
  userId: "user_123",
  apiUrl: "https://api.example.com"
});
```

### `destroy()`

Remove the widget from the page.

```javascript
window.CourseCompanion.destroy();
```

### `updateConfig(newConfig)`

Update configuration after initialization.

```javascript
window.CourseCompanion.updateConfig({
  theme: "dark"
});
```

### `getConfig()`

Get current configuration.

```javascript
const config = window.CourseCompanion.getConfig();
console.log(config);
```

### `isInitialized()`

Check if widget is initialized.

```javascript
if (window.CourseCompanion.isInitialized()) {
  console.log("Widget is running");
}
```

---

## 🎭 Views

### Discovery View (👥)

- Course browsing
- AI-powered recommendations
- "I Know What I Want" vs "Help Me Decide"

### Search View (🔍)

- Search bar with filters
- Real-time results
- Category filtering
- Course cards

### Chat View (💬)

- RAG-powered chatbot
- Message history
- Quick actions (Notes, Quiz, Mind Map, Artifacts)
- File attachments

---

## 🎨 Customization

### Theming

The widget supports light and dark themes:

```javascript
window.CourseCompanion.init({
  theme: "dark" // or "light"
});
```

### Positioning

Choose where the widget appears:

```javascript
window.CourseCompanion.init({
  position: "bottom-right" // bottom-left, top-right, top-left
});
```

---

## 🧪 Development

### Development Mode

```bash
npm run dev
```

Auto-initializes with dev configuration at `http://localhost:5173`

### Build

```bash
npm run build
```

Outputs single-file bundle to `dist/coursecompanion-widget.iife.js`

### Preview Production Build

```bash
npm run preview
```

---

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ❌ IE 11 (Shadow DOM not supported)

---

## 🔐 Security

- Shadow DOM isolation prevents style conflicts
- No access to host page cookies/localStorage
- Sandboxed execution context
- Secure API communication

---

## 📊 Performance

- Bundle size: ~300KB (gzipped)
- Initial load: <2 seconds
- Tree-shaking enabled
- Code splitting for views

---

## 🐛 Troubleshooting

### Widget not appearing?

1. Check browser console for errors
2. Verify script is loaded: `console.log(window.CourseCompanion)`
3. Check Shadow DOM support: `!!document.body.attachShadow`

### Styles not working?

- Widget uses Shadow DOM for isolation
- Host page styles don't affect widget
- Use browser DevTools to inspect shadow root

### API not connecting?

1. Check `apiUrl` configuration
2. Verify CORS settings on backend
3. Check network tab for failed requests

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🔗 Links

- [Documentation](https://docs.coursecompanion.com)
- [API Reference](https://api.coursecompanion.com/docs)
- [Backend Repository](https://github.com/coursecompanion/backend)
- [Support](https://support.coursecompanion.com)

---

## 💬 Support

For questions and support:

- 📧 Email: support@coursecompanion.com
- 💬 Discord: [Join our server](https://discord.gg/coursecompanion)
- 🐛 Issues: [GitHub Issues](https://github.com/coursecompanion/widget/issues)

---

**Built with ❤️ by the CourseCompanion Team**
