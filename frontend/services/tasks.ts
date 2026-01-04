import apiClient from '@/lib/api'
import { Task } from '@/types/task'

export const getTasks = async (): Promise<Task[]> => {
  const response = await apiClient.get('/tasks/')
  return response.data
}

export const createTask = async (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Task> => {
  const response = await apiClient.post('/tasks/', taskData)
  return response.data
}

export const updateTask = async (id: string, taskData: Partial<Task>): Promise<Task> => {
  const response = await apiClient.put(`/tasks/${id}`, taskData)
  return response.data
}

export const deleteTask = async (id: string): Promise<void> => {
  await apiClient.delete(`/tasks/${id}`)
}

export const toggleTaskCompletion = async (id: string): Promise<Task> => {
  const response = await apiClient.patch(`/tasks/${id}/toggle`)
  return response.data
}