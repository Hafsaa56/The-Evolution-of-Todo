import { useAuth } from '@/context/AuthContext'

// This is a wrapper hook that simply re-exports the context hook
// In a more complex app, this could add additional functionality
export const useAuthHook = () => {
  return useAuth()
}