export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: string;
  name: string;
  user_id: number;
  created_at: string;
  usage_count?: number;
}

export interface RecurringTaskPattern {
  id: string;
  base_task_title: string;
  base_task_description?: string;
  recurrence_type: 'daily' | 'weekly' | 'monthly' | 'custom';
  interval: number;
  start_date: string;
  end_date?: string;
  weekdays_mask?: number;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface Reminder {
  id: string;
  task_id: string;
  due_datetime: string;
  reminder_datetime: string;
  sent: boolean;
  snoozed_until?: string;
  dismissed: boolean;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'done';
  priority: 'low' | 'medium' | 'high';
  user_id: number;
  due_date?: string; // Optional due date
  created_at: string;
  updated_at: string;
  completed_at?: string;
  reminder_offset?: number; // Minutes before due_date to send reminder
  tags: Tag[];
  recurring_pattern_id?: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string; // Optional due date
  reminder_offset?: number; // Minutes before due_date to send reminder
  tags?: string[]; // Array of tag names
  recurring_pattern?: {
    recurrence_type: 'daily' | 'weekly' | 'monthly' | 'custom';
    interval: number;
    start_date: string;
    end_date?: string;
    weekdays_mask?: number;
  };
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  status?: 'todo' | 'in_progress' | 'done';
  due_date?: string;
  reminder_offset?: number; // Minutes before due_date to send reminder
  completed?: boolean;
  tags?: string[]; // Array of tag names
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
}