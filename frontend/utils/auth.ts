// Utility functions for authentication token management

export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token)
  }
}

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token')
  }
  return null
}

export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token')
  }
}

export const isAuthenticated = (): boolean => {
  const token = getToken()
  return token !== null && token !== undefined && token !== ''
}