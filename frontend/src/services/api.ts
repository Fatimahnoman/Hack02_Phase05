import axios, { AxiosResponse } from 'axios';
import { 
  AuthResponse, 
  LoginCredentials, 
  RegisterCredentials, 
  Todo, 
  TodoCreate, 
  TodoUpdate,
  Task,
  TaskCreate,
  TaskUpdate,
  Tag,
  RecurringTaskPattern,
  Reminder
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (credentials: RegisterCredentials): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/api/auth/register', credentials),

  login: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/api/auth/login', { email, password }),

  logout: () => {
    localStorage.removeItem('access_token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  }
};

// Todo API calls (backward compatibility)
export const todoAPI = {
  getAll: (): Promise<AxiosResponse<Todo[]>> =>
    api.get('/api/v1/todos/'),

  create: (todo: TodoCreate): Promise<AxiosResponse<Todo>> =>
    api.post('/api/v1/todos/', todo),

  update: (id: number, todo: TodoUpdate): Promise<AxiosResponse<Todo>> =>
    api.put(`/api/v1/todos/${id}`, todo),

  delete: (id: number): Promise<AxiosResponse<void>> =>
    api.delete(`/api/v1/todos/${id}`),

  toggleComplete: (id: number, completed: boolean): Promise<AxiosResponse<{ id: number; completed: boolean }>> =>
    api.patch(`/api/v1/todos/${id}/status`, { completed }),

  getById: (id: number): Promise<AxiosResponse<Todo>> =>
    api.get(`/api/v1/todos/${id}`)
};

// Task API calls (Phase V features)
export const taskAPI = {
  // Basic task operations with new features
  getAll: (params?: {
    priority?: string;
    tag?: string[];
    due_date_from?: string;
    due_date_to?: string;
    without_due_date?: boolean;
    status?: string;
    sort_by?: string;
    sort_order?: string;
    page?: number;
    limit?: number;
  }): Promise<AxiosResponse<{ tasks: Task[], pagination: any }>> =>
    api.get('/api/v1/tasks/', { params }),

  getById: (id: string): Promise<AxiosResponse<Task>> =>
    api.get(`/api/v1/tasks/${id}`),

  create: (task: TaskCreate): Promise<AxiosResponse<Task>> =>
    api.post('/api/v1/tasks/', task),

  update: (id: string, task: TaskUpdate): Promise<AxiosResponse<Task>> =>
    api.put(`/api/v1/tasks/${id}`, task),

  delete: (id: string): Promise<AxiosResponse<void>> =>
    api.delete(`/api/v1/tasks/${id}`),

  updateStatus: (id: string, completed: boolean): Promise<AxiosResponse<Task>> =>
    api.patch(`/api/v1/tasks/${id}/status`, { completed }),

  // Search, filter, sort
  search: (query: string, filters?: {
    priority?: string;
    tag?: string[];
    status?: string;
    sort_by?: string;
    sort_order?: string;
    page?: number;
    limit?: number;
  }): Promise<AxiosResponse<{ tasks: Task[], pagination: any, search_info: any }>> => {
    const params: any = { q: query, ...filters };
    return api.get('/api/v1/tasks/search', { params });
  },
};

// Tag API functions
export const tagAPI = {
  getAll: (): Promise<AxiosResponse<{ tags: Tag[] }>> =>
    api.get('/api/v1/tags'),

  create: (tag: { name: string }): Promise<AxiosResponse<Tag>> =>
    api.post('/api/v1/tags', tag),
};

// Recurring task API functions
export const recurringTaskAPI = {
  getAllPatterns: (): Promise<AxiosResponse<{ patterns: RecurringTaskPattern[] }>> =>
    api.get('/api/v1/recurring-patterns'),

  createPattern: (pattern: Omit<RecurringTaskPattern, 'id' | 'created_at' | 'updated_at'>): Promise<AxiosResponse<RecurringTaskPattern>> =>
    api.post('/api/v1/recurring-patterns', pattern),

  getPatternById: (id: string): Promise<AxiosResponse<RecurringTaskPattern>> =>
    api.get(`/api/v1/recurring-patterns/${id}`),

  updatePattern: (id: string, pattern: Partial<Omit<RecurringTaskPattern, 'id' | 'created_at' | 'user_id'>>): Promise<AxiosResponse<RecurringTaskPattern>> =>
    api.put(`/api/v1/recurring-patterns/${id}`, pattern),

  deletePattern: (id: string): Promise<AxiosResponse<void>> =>
    api.delete(`/api/v1/recurring-patterns/${id}`),
};

// Reminder API functions
export const reminderAPI = {
  getUpcoming: (hoursAhead?: number): Promise<AxiosResponse<{ reminders: Reminder[] }>> =>
    api.get('/api/v1/reminders/upcoming', { params: { hours_ahead: hoursAhead } }),

  snooze: (id: string, minutes: number): Promise<AxiosResponse<Reminder>> =>
    api.post(`/api/v1/reminders/${id}/snooze`, { minutes }),

  dismiss: (id: string): Promise<AxiosResponse<Reminder>> =>
    api.post(`/api/v1/reminders/${id}/dismiss`),
};

export default api;