'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/context/AuthContext'
import { Task } from '@/types/task'
import { TaskForm } from '@/components/tasks/TaskForm'
import { TaskList } from '@/components/tasks/TaskList'
import { getTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '@/services/tasks'
import { useRouter } from 'next/navigation'

export default function Dashboard() {
  const { user, loading, logout } = useAuth()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loadingTasks, setLoadingTasks] = useState(true)
  const [isLoaded, setIsLoaded] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsLoaded(true)
    if (!loading && !user) {
      router.push('/login')
    } else if (user) {
      fetchTasks()
    }
  }, [user, loading, router])

  const fetchTasks = async () => {
    try {
      setLoadingTasks(true)
      const tasksData = await getTasks()
      setTasks(tasksData)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoadingTasks(false)
    }
  }

  const [creatingTask, setCreatingTask] = useState(false)
  const [updatingTask, setUpdatingTask] = useState<string | null>(null)
  const [deletingTask, setDeletingTask] = useState<string | null>(null)

  const handleCreateTask = async (title: string, description: string) => {
    try {
      setCreatingTask(true)
      const newTask = await createTask({ title, description, completed: false })
      setTasks([newTask, ...tasks])
    } catch (error) {
      console.error('Failed to create task:', error)
    } finally {
      setCreatingTask(false)
    }
  }

  const handleUpdateTask = async (id: string, title: string, description: string) => {
    try {
      setUpdatingTask(id)
      const updatedTask = await updateTask(id, { title, description })
      setTasks(tasks.map(task => task.id === id ? updatedTask : task))
    } catch (error) {
      console.error('Failed to update task:', error)
    } finally {
      setUpdatingTask(null)
    }
  }

  const handleDeleteTask = async (id: string) => {
    try {
      setDeletingTask(id)
      await deleteTask(id)
      setTasks(tasks.filter(task => task.id !== id))
    } catch (error) {
      console.error('Failed to delete task:', error)
    } finally {
      setDeletingTask(null)
    }
  }

  const handleToggleTaskCompletion = async (id: string) => {
    try {
      setUpdatingTask(id)
      const taskToToggle = tasks.find(task => task.id === id)
      if (taskToToggle) {
        const updatedTask = await toggleTaskCompletion(id)
        setTasks(tasks.map(task => task.id === id ? updatedTask : task))
      }
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
    } finally {
      setUpdatingTask(null)
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-white border-opacity-50"></div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  const completedCount = tasks.filter(t => t.completed).length
  const pendingCount = tasks.length - completedCount

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-lg shadow-sm border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                TodoApp
              </span>
            </div>
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-3 px-4 py-2 bg-white/50 rounded-full border border-white/50">
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-400 rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {user.email[0].toUpperCase()}
                </div>
                <span className="text-gray-700 font-medium text-sm truncate max-w-[150px]">{user.email}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto py-8 px-4">
        {/* Welcome Section */}
        <div className={`mb-8 transition-all duration-700 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-3xl p-8 text-white shadow-2xl">
            <h1 className="text-3xl font-bold mb-2">Welcome back! 👋</h1>
            <p className="text-white/80">Ready to tackle your tasks today?</p>
          </div>
        </div>

        {/* Stats Cards */}
        <div className={`grid grid-cols-3 gap-4 mb-8 transition-all duration-700 delay-100 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Tasks</p>
                <p className="text-2xl font-bold text-gray-900">{tasks.length}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-500">Completed</p>
                <p className="text-2xl font-bold text-gray-900">{completedCount}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-500">Pending</p>
                <p className="text-2xl font-bold text-gray-900">{pendingCount}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Task Form */}
        <div className={`mb-8 transition-all duration-700 delay-200 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <TaskForm
            onCreateTask={handleCreateTask}
            creatingTask={creatingTask}
          />
        </div>

        {/* Task List */}
        <div className={`transition-all duration-700 delay-300 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          {loadingTasks ? (
            <div className="bg-white rounded-3xl p-12 shadow-lg text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-200 border-t-indigo-500 mx-auto mb-4"></div>
              <p className="text-gray-500">Loading your tasks...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="bg-white rounded-3xl p-12 shadow-lg text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks yet!</h3>
              <p className="text-gray-500">Create your first task above to get started.</p>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
              onToggleTaskCompletion={handleToggleTaskCompletion}
              updatingTask={updatingTask}
              deletingTask={deletingTask}
            />
          )}
        </div>
      </main>
    </div>
  )
}
