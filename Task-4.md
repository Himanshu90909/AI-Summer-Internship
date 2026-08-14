# Task - 4: Advanced Task Management Application

## Project Overview
A modern, feature-rich task management application built with React and TailwindCSS. This app allows users to create, manage, prioritize, and track their tasks efficiently with a beautiful and intuitive interface.

## Features

### Core Features
1. **Create Tasks** - Add new tasks with title and description
2. **Task Categories** - Organize tasks by categories (Work, Personal, Shopping, Health, etc.)
3. **Priority Levels** - Set priority (High, Medium, Low) for each task
4. **Due Dates** - Assign due dates to tasks
5. **Status Tracking** - Mark tasks as Pending, In Progress, or Completed
6. **Edit Tasks** - Modify existing task details
7. **Delete Tasks** - Remove tasks from the list
8. **Search & Filter** - Find tasks by keywords, category, or priority
9. **Task Statistics** - View dashboard with task completion stats
10. **Local Storage** - Persist tasks in browser local storage

### Advanced Features
1. **Recurring Tasks** - Set tasks to repeat daily, weekly, or monthly
2. **Task Tags** - Add multiple tags to tasks for better organization
3. **Notifications** - Get reminders for upcoming due dates
4. **Dark/Light Mode** - Toggle between dark and light themes
5. **Export Tasks** - Download tasks as JSON or CSV
6. **Drag & Drop** - Reorder tasks by dragging
7. **Task Notes** - Add detailed notes to tasks
8. **Time Tracking** - Track time spent on tasks

## Tech Stack
- **Frontend**: React 18
- **Styling**: TailwindCSS
- **Build Tool**: Vite
- **State Management**: React Hooks (useState, useContext)
- **Storage**: Browser Local Storage
- **Icons**: Unicode Emojis

## Project Structure

```
task-management-app/
├── src/
│   ├── components/
│   │   ├── TaskForm.jsx
│   │   ├── TaskList.jsx
│   │   ├── TaskItem.jsx
│   │   ├── TaskFilter.jsx
│   │   ├── TaskStats.jsx
│   │   └── TaskModal.jsx
│   ├── context/
│   │   └── TaskContext.jsx
│   ├── hooks/
│   │   └── useLocalStorage.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Himanshu90909/AI-Summer-Internship.git
cd AI-Summer-Internship

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## How to Use

### Adding a Task
1. Enter task title in the input field
2. (Optional) Add description, category, priority, and due date
3. Click "Add Task" button
4. Task will appear in the task list

### Managing Tasks
- **Edit**: Click the edit icon to modify task details
- **Complete**: Click the checkbox to mark task as completed
- **Delete**: Click the trash icon to remove the task
- **Filter**: Use filter options to view specific tasks

### Organizing Tasks
- **By Category**: Filter tasks by Work, Personal, Shopping, etc.
- **By Priority**: View High, Medium, or Low priority tasks
- **By Status**: Show Pending, In Progress, or Completed tasks
- **Search**: Use the search bar to find tasks by keywords

### Dashboard
- View total tasks count
- See completed tasks percentage
- Check upcoming due dates
- View tasks by category breakdown

## Key Components

### TaskForm Component
Handles task creation with fields for:
- Task title (required)
- Description (optional)
- Category selection
- Priority level
- Due date picker
- Recurring option

### TaskList Component
Displays all tasks with:
- Task items in organized layout
- Filter and search functionality
- Sorting options
- Task statistics

### TaskItem Component
Individual task display with:
- Checkbox for completion status
- Task title and description
- Category badge
- Priority indicator
- Due date display
- Action buttons (edit, delete)

### TaskFilter Component
Filtering and search features:
- Category filter
- Priority filter
- Status filter
- Search by keywords
- Sort options

### TaskStats Component
Dashboard showing:
- Total tasks count
- Completed tasks count
- Completion percentage
- Tasks by category
- Overdue tasks

## State Management

Using React Context API for global state:
- Tasks array
- Filter settings
- Theme preference
- Notification settings

## Local Storage

Tasks are automatically saved to browser local storage:
- Persists across browser sessions
- Automatic sync on task changes
- Export/Import functionality

## Keyboard Shortcuts

- `Ctrl/Cmd + N` - New task
- `Ctrl/Cmd + F` - Focus search
- `Ctrl/Cmd + S` - Save/Export
- `Esc` - Close modals

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance Optimizations

- Lazy loading of components
- Memoization of expensive computations
- Virtual scrolling for large task lists
- Debounced search functionality
- Optimized re-renders

## Future Enhancements

1. **Cloud Sync** - Sync tasks across devices
2. **Collaboration** - Share tasks with team members
3. **AI Suggestions** - Smart task recommendations
4. **Voice Input** - Create tasks by voice
5. **Mobile App** - React Native version
6. **Calendar View** - Visual calendar display
7. **Subtasks** - Break tasks into smaller steps
8. **Attachments** - Add files to tasks
9. **Webhooks** - Integrate with other services
10. **API** - RESTful API for external access

## Code Examples

### Creating a Task
```javascript
const addTask = (taskData) => {
  const newTask = {
    id: Date.now(),
    title: taskData.title,
    description: taskData.description,
    category: taskData.category,
    priority: taskData.priority,
    dueDate: taskData.dueDate,
    status: 'pending',
    createdAt: new Date(),
    completed: false
  };
  setTasks([...tasks, newTask]);
};
```

### Filtering Tasks
```javascript
const filteredTasks = tasks.filter(task => {
  return (
    (filterCategory === 'all' || task.category === filterCategory) &&
    (filterPriority === 'all' || task.priority === filterPriority) &&
    (filterStatus === 'all' || task.status === filterStatus) &&
    (searchTerm === '' || task.title.toLowerCase().includes(searchTerm.toLowerCase()))
  );
});
```

### Saving to Local Storage
```javascript
useEffect(() => {
  localStorage.setItem('tasks', JSON.stringify(tasks));
}, [tasks]);
```

## API Integration (Future)

```javascript
// Example API endpoints
GET /api/tasks - Get all tasks
POST /api/tasks - Create new task
PUT /api/tasks/:id - Update task
DELETE /api/tasks/:id - Delete task
GET /api/tasks/stats - Get statistics
POST /api/tasks/export - Export tasks
```

## Security Considerations

- Input validation and sanitization
- XSS prevention
- CSRF protection
- Secure local storage handling
- Data encryption for sensitive information

## Testing

```bash
# Run tests
npm run test

# Coverage report
npm run test:coverage
```

## Deployment

```bash
# Build production
npm run build

# Deploy to Vercel
vercel deploy

# Deploy to Netlify
netlify deploy --prod
```

## License

MIT License - See LICENSE file for details

## Author

Smart Intelligence by Himanshu

## Support

For issues, suggestions, or contributions, please visit:
https://github.com/Himanshu90909/AI-Summer-Internship

---

**Last Updated**: July 19, 2026
**Version**: 1.0.0
**Status**: Complete
