'use client'

import { useState } from 'react'
import { Task } from '@/types/task'
import { TaskItem } from '@/components/tasks/TaskItem'

type TaskListProps = {
  tasks: Task[]
  onUpdateTask: (id: string, title: string, description: string) => void
  onDeleteTask: (id: string) => void
  onToggleTaskCompletion: (id: string) => void
  updatingTask?: string | null
  deletingTask?: string | null
}

export const TaskList = ({ tasks, onUpdateTask, onDeleteTask, onToggleTaskCompletion, updatingTask, deletingTask }: TaskListProps) => {
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id)
    setEditTitle(task.title)
    setEditDescription(task.description)
  }

  const cancelEditing = () => {
    setEditingTaskId(null)
    setEditTitle('')
    setEditDescription('')
  }

  const saveEditing = (id: string) => {
    onUpdateTask(id, editTitle, editDescription)
    cancelEditing()
  }

  const completedTasks = tasks.filter(t => t.completed)
  const pendingTasks = tasks.filter(t => !t.completed)

  return (
    <div className="space-y-6">
      {/* Tasks Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          Your Tasks
        </h2>
        <div className="flex items-center gap-4">
          <span className="px-4 py-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 rounded-full text-sm font-medium">
            {pendingTasks.length} pending
          </span>
          <span className="px-4 py-2 bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 rounded-full text-sm font-medium">
            {completedTasks.length} completed
          </span>
        </div>
      </div>

      {/* Tasks Container */}
      <div className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden">
        {tasks.length === 0 ? (
          <div className="p-12 text-center">
            <div className="w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-12 h-12 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks yet!</h3>
            <p className="text-gray-500">Create your first task above to get started.</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-100">
            {tasks.map((task) => (
              <li key={task.id}>
                {editingTaskId === task.id ? (
                  <div className="p-6 bg-gradient-to-r from-indigo-50/50 to-purple-50/50">
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </div>
                      <span className="font-medium text-indigo-700">Editing Task</span>
                    </div>
                    <div className="space-y-4">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100/50 transition-all"
                        placeholder="Task title"
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100/50 transition-all resize-none"
                        rows={2}
                        placeholder="Task description"
                      />
                    </div>
                    <div className="mt-4 flex gap-3">
                      <button
                        onClick={() => saveEditing(task.id)}
                        className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl font-medium hover:shadow-lg hover:scale-[1.02] transition-all"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Save Changes
                      </button>
                      <button
                        onClick={cancelEditing}
                        className="flex items-center gap-2 px-5 py-2.5 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200 transition-all"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <TaskItem
                    task={task}
                    onEdit={startEditing}
                    onDelete={onDeleteTask}
                    onToggleCompletion={onToggleTaskCompletion}
                    isUpdating={updatingTask === task.id}
                    isDeleting={deletingTask === task.id}
                  />
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
