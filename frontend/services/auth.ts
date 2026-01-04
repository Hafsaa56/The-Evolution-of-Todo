import axios from 'axios';

type LoginCredentials = {
  email: string;
  password: string;
};

type RegisterData = {
  email: string;
  password: string;
};

type TokenResponse = {
  access_token: string;
  token_type: string;
};

// Create an axios instance without auth interceptor for auth requests
const authApiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = async (credentials: LoginCredentials): Promise<TokenResponse> => {
  const response = await authApiClient.post('/auth/login', credentials);
  return response.data;
};

export const register = async (userData: RegisterData): Promise<TokenResponse> => {
  const response = await authApiClient.post('/auth/register', userData);
  return response.data;
};

export const getProfile = async (): Promise<any> => {
  // This will need the auth header, so we'll use the regular apiClient
  const token = localStorage.getItem('access_token');
  const response = await axios.get('/api/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.data;
};