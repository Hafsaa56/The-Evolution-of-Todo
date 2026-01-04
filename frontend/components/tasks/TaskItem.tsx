'use client'

import { Task } from '@/types/task'

type TaskItemProps = {
  task: Task
  onEdit: (task: Task) => void
  onDelete: (id: string) => void
  onToggleCompletion: (id: string) => void
  isUpdating?: boolean
  isDeleting?: boolean
}

export const TaskItem = ({ task, onEdit, onDelete, onToggleCompletion, isUpdating, isDeleting }: TaskItemProps) => {
  const handleToggle = () => {
    if (!isUpdating && !isDeleting) {
      onToggleCompletion(task.id)
    }
  }

  const handleEdit = () => {
    if (!isUpdating && !isDeleting) {
      onEdit(task)
    }
  }

  const handleDelete = () => {
    if (!isUpdating && !isDeleting) {
      onDelete(task.id)
    }
  }

  return (
    <div className={`p-5 hover:bg-gray-50/50 transition-all duration-200 ${isUpdating || isDeleting ? 'opacity-50' : ''}`}>
      <div className="flex items-start gap-4">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isUpdating || isDeleting}
          className={`mt-0.5 flex-shrink-0 w-6 h-6 rounded-xl border-2 flex items-center justify-center transition-all duration-200 ${
            task.completed
              ? 'bg-gradient-to-r from-green-500 to-emerald-500 border-green-500'
              : 'border-gray-300 hover:border-indigo-400 hover:bg-indigo-50'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          {task.completed && (
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <p className={`text-lg font-medium transition-all duration-200 ${
                task.completed
                  ? 'line-through text-gray-400'
                  : 'text-gray-900'
              }`}>
                {task.title}
              </p>
              {task.description && (
                <p className={`mt-1 text-sm transition-all duration-200 ${
                  task.completed
                    ? 'text-gray-300'
                    : 'text-gray-500'
                }`}>
                  {task.description}
                </p>
              )}
              {/* Date */}
              <div className="mt-3 flex items-center gap-4 text-xs">
                <span className={`flex items-center gap-1 ${
                  task.completed ? 'text-gray-400' : 'text-gray-400'
                }`}>
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </span>
                {task.updated_at !== task.created_at && (
                  <span className={`flex items-center gap-1 ${
                    task.completed ? 'text-gray-400' : 'text-gray-400'
                  }`}>
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Updated: {new Date(task.updated_at).toLocaleDateString()}
                  </span>
                )}
                {/* Status Badge */}
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.completed
                    ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700'
                    : 'bg-gradient-to-r from-yellow-100 to-orange-100 text-orange-700'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <button
                onClick={handleEdit}
                disabled={isUpdating || isDeleting}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 rounded-lg text-sm font-medium hover:from-indigo-200 hover:to-purple-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isUpdating ? (
                  <>
                    <svg className="animate-spin h-3.5 w-3.5 text-indigo-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Updating...
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit
                  </>
                )}
              </button>
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-red-100 to-pink-100 text-red-700 rounded-lg text-sm font-medium hover:from-red-200 hover:to-pink-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isDeleting ? (
                  <>
                    <svg className="animate-spin h-3.5 w-3.5 text-red-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Deleting...
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Delete
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
