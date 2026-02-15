import React from 'react';
import { Todo, TodoUpdate, Task, TaskUpdate } from '../../types';
import TodoItem from './TodoItem';

// Define a unified interface for both todos and tasks
interface UnifiedItem {
  id: string | number;
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
  created_at: string;
  updated_at: string;
  user_id: number;
  type: 'todo' | 'task';
  originalId: string | number;
  // Task-specific fields
  status?: string;
  priority?: string;
  completed_at?: string | null;
  reminder_offset?: number;
  tags?: any[]; // Simplified for compatibility
}

interface TodoListProps {
  todos: UnifiedItem[];
  onToggle: (id: string | number, completed: boolean) => void;
  onUpdate: (id: string | number, updates: TodoUpdate | TaskUpdate) => void;
  onDelete: (id: string | number) => void;
  emptyState?: React.ReactNode;
}

const TodoList = ({ todos, onToggle, onUpdate, onDelete, emptyState }: TodoListProps) => {
  if (todos.length === 0) {
    return emptyState || <div className="empty-state">No tasks yet. Add one to get started!</div>;
  }

  return (
    <div className="todo-list">
      <div className="list-header">
        <h2>My Tasks</h2>
        <span className="task-count">{todos.length} {todos.length === 1 ? 'task' : 'tasks'}</span>
      </div>

      {todos.map((item) => (
        <TodoItem
          key={item.originalId}
          todo={{
            ...item,
            id: typeof item.id === 'number' ? item.id : parseInt(item.id) || 0
          }}
          onToggle={(id, completed) => onToggle(item.originalId, completed)}
          onUpdate={(id, updates) => onUpdate(item.originalId, updates)}
          onDelete={(id) => onDelete(item.originalId)}
        />
      ))}

      <style jsx>{`
        .todo-list {
          display: flex;
          flex-direction: column;
          background: var(--card-bg);
          border-radius: var(--border-radius);
          padding: 25px;
          border: 1px solid var(--card-border);
          margin-top: 20px;
        }

        .list-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
          padding-bottom: 15px;
          border-bottom: 1px solid var(--card-border);
        }

        .list-header h2 {
          margin: 0;
          font-size: 24px;
          font-weight: 700;
          color: var(--text-primary);
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .task-count {
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          padding: 6px 15px;
          border-radius: 20px;
          font-size: 0.95rem;
          font-weight: 600;
        }

        @media (max-width: 768px) {
          .list-header {
            flex-direction: column;
            gap: 12px;
            align-items: flex-start;
          }

          .task-count {
            align-self: flex-start;
          }

          .todo-list {
            padding: 20px 15px;
          }
        }

        @media (max-width: 480px) {
          .list-header {
            gap: 10px;
          }

          .list-header h2 {
            font-size: 20px;
          }

          .task-count {
            font-size: 0.9rem;
            padding: 5px 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoList;