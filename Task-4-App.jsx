import { useState, useEffect, useContext, createContext } from 'react'
import './TaskApp.css'

// Task Context
const TaskContext = createContext()

// Main App Component
export default function TaskManagementApp() {
  const [tasks, setTasks] = useState([])
  const [filterCategory, setFilterCategory] = useState('all')
  const [filterPriority, setFilterPriority] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [darkMode, setDarkMode] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState(null)

  // Load tasks from localStorage
  useEffect(() => {
    const savedTasks = localStorage.getItem('tasks')
    if (savedTasks) {
      setTasks(JSON.parse(savedTasks))
    }
  }, [])

  // Save tasks to localStorage
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks))
  }, [tasks])

  // Add or update task
  const handleAddTask = (taskData) => {
    if (editingTask) {
      setTasks(tasks.map(t => t.id === editingTask.id ? { ...taskData, id: editingTask.id } : t))
      setEditingTask(null)
    } else {
      const newTask = {
        ...taskData,
        id: Date.now(),
        createdAt: new Date().toISOString()
      }
      setTasks([...tasks, newTask])
    }
    setShowForm(false)
  }

  // Delete task
  const handleDeleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id))
  }

  // Toggle task completion
  const handleToggleComplete = (id) => {
    setTasks(tasks.map(t => 
      t.id === id ? { ...t, completed: !t.completed, status: !t.completed ? 'completed' : 'pending' } : t
    ))
  }

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    return (
      (filterCategory === 'all' || task.category === filterCategory) &&
      (filterPriority === 'all' || task.priority === filterPriority) &&
      (filterStatus === 'all' || task.status === filterStatus) &&
      (searchTerm === '' || task.title.toLowerCase().includes(searchTerm.toLowerCase()))
    )
  })

  // Calculate statistics
  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    pending: tasks.filter(t => !t.completed).length,
    completionPercentage: tasks.length > 0 ? Math.round((tasks.filter(t => t.completed).length / tasks.length) * 100) : 0
  }

  return (
    <TaskContext.Provider value={{ tasks, setTasks }}>
      <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
        {/* Header */}
        <header className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b shadow-sm`}>
          <div className="max-w-6xl mx-auto px-4 py-6 flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">📋 Task Manager</h1>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Smart Intelligence by Himanshu</p>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${darkMode ? 'bg-yellow-500 text-gray-900' : 'bg-gray-800 text-white'}`}
            >
              {darkMode ? '☀️ Light' : '🌙 Dark'}
            </button>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-4 py-8">
          {/* Statistics Dashboard */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <StatCard icon="📊" label="Total Tasks" value={stats.total} darkMode={darkMode} />
            <StatCard icon="✅" label="Completed" value={stats.completed} darkMode={darkMode} />
            <StatCard icon="⏳" label="Pending" value={stats.pending} darkMode={darkMode} />
            <StatCard icon="📈" label="Progress" value={`${stats.completionPercentage}%`} darkMode={darkMode} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <aside className={`lg:col-span-1 ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-md h-fit`}>
              <h2 className="text-xl font-bold mb-4">🔍 Filters</h2>

              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Search</label>
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className={`w-full px-3 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                />
              </div>

              {/* Category Filter */}
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Category</label>
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className={`w-full px-3 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  <option value="all">All Categories</option>
                  <option value="work">💼 Work</option>
                  <option value="personal">👤 Personal</option>
                  <option value="shopping">🛒 Shopping</option>
                  <option value="health">❤️ Health</option>
                  <option value="learning">📚 Learning</option>
                </select>
              </div>

              {/* Priority Filter */}
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Priority</label>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className={`w-full px-3 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  <option value="all">All Priorities</option>
                  <option value="high">🔴 High</option>
                  <option value="medium">🟡 Medium</option>
                  <option value="low">🟢 Low</option>
                </select>
              </div>

              {/* Status Filter */}
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Status</label>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className={`w-full px-3 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  <option value="all">All Status</option>
                  <option value="pending">⏳ Pending</option>
                  <option value="in-progress">🔄 In Progress</option>
                  <option value="completed">✅ Completed</option>
                </select>
              </div>

              {/* Clear Filters */}
              <button
                onClick={() => {
                  setFilterCategory('all')
                  setFilterPriority('all')
                  setFilterStatus('all')
                  setSearchTerm('')
                }}
                className="w-full px-4 py-2 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition"
              >
                Clear Filters
              </button>
            </aside>

            {/* Main Content */}
            <section className="lg:col-span-3">
              {/* Add Task Button */}
              <button
                onClick={() => {
                  setShowForm(!showForm)
                  setEditingTask(null)
                }}
                className="mb-6 px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition"
              >
                {showForm ? '✕ Cancel' : '+ Add New Task'}
              </button>

              {/* Task Form */}
              {showForm && (
                <TaskForm onSubmit={handleAddTask} editingTask={editingTask} darkMode={darkMode} />
              )}

              {/* Task List */}
              <div className="space-y-4">
                {filteredTasks.length > 0 ? (
                  filteredTasks.map(task => (
                    <TaskItem
                      key={task.id}
                      task={task}
                      onToggle={() => handleToggleComplete(task.id)}
                      onDelete={() => handleDeleteTask(task.id)}
                      onEdit={() => {
                        setEditingTask(task)
                        setShowForm(true)
                      }}
                      darkMode={darkMode}
                    />
                  ))
                ) : (
                  <div className={`text-center py-12 ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg`}>
                    <p className="text-2xl mb-2">📭</p>
                    <p className={`text-lg font-semibold ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>No tasks found</p>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Create a new task to get started</p>
                  </div>
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </TaskContext.Provider>
  )
}

// Task Form Component
function TaskForm({ onSubmit, editingTask, darkMode }) {
  const [formData, setFormData] = useState(editingTask || {
    title: '',
    description: '',
    category: 'personal',
    priority: 'medium',
    dueDate: '',
    status: 'pending'
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.title.trim()) {
      onSubmit(formData)
      setFormData({ title: '', description: '', category: 'personal', priority: 'medium', dueDate: '', status: 'pending' })
    }
  }

  return (
    <form onSubmit={handleSubmit} className={`mb-6 p-6 rounded-lg shadow-md ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Task Title *</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder="Enter task title..."
            className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Category</label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
          >
            <option value="work">💼 Work</option>
            <option value="personal">👤 Personal</option>
            <option value="shopping">🛒 Shopping</option>
            <option value="health">❤️ Health</option>
            <option value="learning">📚 Learning</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Priority</label>
          <select
            value={formData.priority}
            onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
            className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
          >
            <option value="low">🟢 Low</option>
            <option value="medium">🟡 Medium</option>
            <option value="high">🔴 High</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Due Date</label>
          <input
            type="date"
            value={formData.dueDate}
            onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
            className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Status</label>
          <select
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
          >
            <option value="pending">⏳ Pending</option>
            <option value="in-progress">🔄 In Progress</option>
            <option value="completed">✅ Completed</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-2">Description</label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Enter task description..."
          rows="3"
          className={`w-full px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
        />
      </div>

      <button
        type="submit"
        className="px-6 py-2 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition"
      >
        {editingTask ? '💾 Update Task' : '➕ Add Task'}
      </button>
    </form>
  )
}

// Task Item Component
function TaskItem({ task, onToggle, onDelete, onEdit, darkMode }) {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-500'
      case 'medium': return 'text-yellow-500'
      case 'low': return 'text-green-500'
      default: return 'text-gray-500'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high': return '🔴'
      case 'medium': return '🟡'
      case 'low': return '🟢'
      default: return '⚪'
    }
  }

  const getCategoryIcon = (category) => {
    const icons = {
      work: '💼',
      personal: '👤',
      shopping: '🛒',
      health: '❤️',
      learning: '📚'
    }
    return icons[category] || '📌'
  }

  return (
    <div className={`p-4 rounded-lg shadow-md ${darkMode ? 'bg-gray-800' : 'bg-white'} flex items-start gap-4 hover:shadow-lg transition`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={onToggle}
        className="mt-1 w-5 h-5 cursor-pointer"
      />
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-2">
          <h3 className={`text-lg font-semibold ${task.completed ? 'line-through opacity-60' : ''}`}>
            {task.title}
          </h3>
          <span className={`text-sm px-2 py-1 rounded ${getPriorityColor(task.priority)} font-semibold`}>
            {getPriorityIcon(task.priority)} {task.priority}
          </span>
          <span className="text-sm px-2 py-1 rounded bg-blue-100 text-blue-800">
            {getCategoryIcon(task.category)} {task.category}
          </span>
        </div>
        {task.description && (
          <p className={`text-sm mb-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            {task.description}
          </p>
        )}
        <div className="flex items-center gap-4 text-sm">
          <span className={`px-2 py-1 rounded ${task.status === 'completed' ? 'bg-green-100 text-green-800' : task.status === 'in-progress' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}>
            {task.status === 'completed' ? '✅ Completed' : task.status === 'in-progress' ? '🔄 In Progress' : '⏳ Pending'}
          </span>
          {task.dueDate && (
            <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              📅 {new Date(task.dueDate).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>
      <div className="flex gap-2">
        <button
          onClick={onEdit}
          className="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          ✏️
        </button>
        <button
          onClick={onDelete}
          className="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
        >
          🗑️
        </button>
      </div>
    </div>
  )
}

// Stat Card Component
function StatCard({ icon, label, value, darkMode }) {
  return (
    <div className={`p-6 rounded-lg shadow-md ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
      <div className="text-3xl mb-2">{icon}</div>
      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  )
}
