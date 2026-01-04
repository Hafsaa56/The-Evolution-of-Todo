'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'

type User = {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('access_token')
    if (token) {
      // Verify token and get user info
      fetchUserInfo()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUserInfo = async () => {
    try {
      const response = await fetch('/api/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        // Token is invalid, clear it
        localStorage.removeItem('access_token')
      }
    } catch (error) {
      console.error('Error fetching user info:', error)
      localStorage.removeItem('access_token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const { access_token } = await import('@/services/auth').then(mod =>
        mod.login({ email, password })
      )

      localStorage.setItem('access_token', access_token)

      // Get user info after login
      await fetchUserInfo()
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || error.message || 'Login failed')
    }
  }

  const register = async (email: string, password: string) => {
    try {
      const { access_token } = await import('@/services/auth').then(mod =>
        mod.register({ email, password })
      )

      localStorage.setItem('access_token', access_token)

      // Get user info after registration
      await fetchUserInfo()
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || error.message || 'Registration failed')
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    router.push('/')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}