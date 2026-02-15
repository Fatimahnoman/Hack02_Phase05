import React, { useState } from 'react';
import { Todo, TodoUpdate, Task, TaskUpdate } from '../../types';

// Define a unified interface for both todos and tasks
interface UnifiedItem extends Todo {
  type: 'todo' | 'task';
  originalId: string | number;
  // Task-specific fields
  status?: string;
  priority?: string;
  completed_at?: string | null;
  reminder_offset?: number;
  tags?: any[]; // Simplified for compatibility
}

interface TodoItemProps {
  todo: UnifiedItem;
  onToggle: (id: string | number, completed: boolean) => void;
  onUpdate: (id: string | number, updates: TodoUpdate | TaskUpdate) => void;
  onDelete: (id: string | number) => void;
}

const TodoItem = ({ todo, onToggle, onUpdate, onDelete }: TodoItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [editPriority, setEditPriority] = useState<'low' | 'medium' | 'high'>(todo.priority || 'medium');
  const [editDueDate, setEditDueDate] = useState(todo.due_date || '');
  const [editStatus, setEditStatus] = useState(todo.status || 'todo');
  const [editTags, setEditTags] = useState<string[]>(todo.tags?.map(tag => tag.name) || []);

  const handleToggle = () => {
    // For todos, we toggle completed status; for tasks, we update status
    if (todo.type === 'todo') {
      onToggle(todo.originalId, !todo.completed);
    } else {
      // For tasks, toggle between 'todo' and 'done' status
      const newStatus = todo.status === 'done' ? 'todo' : 'done';
      onUpdate(todo.originalId, { status: newStatus });
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditPriority(todo.priority || 'medium');
    setEditDueDate(todo.due_date || '');
    setEditStatus(todo.status || 'todo');
    setEditTags(todo.tags?.map(tag => tag.name) || []);
  };

  const handleSave = () => {
    // Determine if this is a todo or task and create appropriate update object
    if (todo.type === 'todo') {
      const updates: TodoUpdate = {
        title: editTitle,
        description: editDescription || undefined,
        due_date: editDueDate || undefined,
        completed: todo.completed  // Preserve current completion status
      };
      onUpdate(todo.originalId, updates);
    } else {
      const updates: TaskUpdate = {
        title: editTitle,
        description: editDescription || undefined,
        priority: editPriority,
        status: editStatus,
        due_date: editDueDate || undefined,
        tags: editTags
      };
      onUpdate(todo.originalId, updates);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reset to original values
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditPriority(todo.priority || 'medium');
    setEditDueDate(todo.due_date || '');
    setEditStatus(todo.status || 'todo');
    setEditTags(todo.tags?.map(tag => tag.name) || []);
  };

  const handleDelete = () => {
    onDelete(todo.originalId);
  };

  // Safe date rendering
  const formatDate = (dateStr?: string) =>
    dateStr ? new Date(dateStr).toLocaleDateString() : 'No date';

  // Format status for display
  const getStatusClass = (status: string) => {
    switch (status) {
      case 'done': return 'status-done';
      case 'in_progress': return 'status-in-progress';
      case 'todo': return 'status-todo';
      default: return 'status-todo'; // Default to todo if undefined
    }
  };

  // Format priority for display
  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return 'priority-medium'; // Default to medium if undefined
    }
  };

  return (
    <div className={`task-item ${(todo.status === 'done' || todo.completed) ? 'completed' : ''}`}>
      <div className="task-content">
        {isEditing ? (
          <div className="edit-form">
            <div className="edit-header">
              <div
                className={`edit-checkbox ${(todo.status === 'done' || todo.completed) ? 'completed' : 'incomplete'}`}
                onClick={handleToggle}
              >
                {(todo.status === 'done' || todo.completed) ? '✓' : '✕'}
              </div>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="edit-title"
                placeholder="Task title"
              />
            </div>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="edit-description"
              placeholder="Task description"
            />
            <div className="edit-row">
              <select
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value as 'low' | 'medium' | 'high')}
                className="edit-priority"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <input
                type="date"
                value={editDueDate}
                onChange={(e) => setEditDueDate(e.target.value)}
                className="edit-date"
              />
              <select
                value={editStatus}
                onChange={(e) => setEditStatus(e.target.value)}
                className="edit-status"
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>
            <div className="edit-tags">
              {editTags.map((tag, index) => (
                <span key={index} className="tag-chip">
                  #{tag}
                  <button
                    type="button"
                    onClick={() => setEditTags(editTags.filter((_, i) => i !== index))}
                    className="remove-tag-btn"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div className="edit-buttons">
              <button onClick={handleSave} className="save-btn btn-primary">
                Save
              </button>
              <button onClick={handleCancel} className="cancel-btn btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="task-header">
              <div
                className={`task-checkbox ${(todo.status === 'done' || todo.completed) ? 'completed' : 'incomplete'}`}
                onClick={handleToggle}
              >
                {(todo.status === 'done' || todo.completed) ? '✓' : '✕'}
              </div>
              <div className="task-text">
                <div className="task-title-row">
                  <h3 className={`task-title ${(todo.status === 'done' || todo.completed) ? 'completed' : ''}`}>
                    {todo.title}
                  </h3>
                  {todo.priority && (
                    <span className={`priority-badge ${getPriorityClass(todo.priority || 'medium')}`}>
                      {todo.priority?.toUpperCase()}
                    </span>
                  )}
                </div>
                {todo.description && (
                  <p className={`task-description ${(todo.status === 'done' || todo.completed) ? 'completed' : ''}`}>
                    {todo.description}
                  </p>
                )}
                <div className="task-meta">
                  {todo.due_date && (
                    <span className={`task-due-date ${(todo.status === 'done' || todo.completed) ? 'completed' : ''}`}>
                      📅 {formatDate(todo.due_date)}
                    </span>
                  )}
                  {!todo.due_date && todo.created_at && (
                    <span className={`task-created ${(todo.status === 'done' || todo.completed) ? 'completed' : ''}`}>
                      📅 Created: {formatDate(todo.created_at)}
                    </span>
                  )}
                  {(todo.status === 'done' || todo.completed) && (
                    <span className="task-completed-badge">✓ Completed</span>
                  )}
                  <span className={`status-badge ${getStatusClass(todo.status || 'todo')}`}>
                    {(todo.status || 'todo').replace('_', ' ').toUpperCase()}
                  </span>
                </div>
                <div className="task-tags">
                  {todo.tags && todo.tags.map((tag: any, index: number) => (
                    <span key={index} className="tag-badge">
                      #{typeof tag === 'string' ? tag : tag.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <div className="task-actions">
              <button onClick={handleEdit} className="edit-btn btn-secondary" title="Edit task">
                ✏️
              </button>
              <button onClick={handleDelete} className="delete-btn btn-danger" title="Delete task">
                🗑️
              </button>
            </div>
          </>
        )}
      </div>

      <style jsx>{`
        .task-item {
          background: var(--card-bg);
          border-radius: var(--border-radius);
          padding: 20px;
          margin-bottom: 16px;
          border: 1px solid var(--card-border);
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .task-item:hover {
          box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
          transform: translateY(-2px);
        }

        .task-item.completed {
          opacity: 0.8;
          background: rgba(16, 185, 129, 0.05);
        }

        .task-content {
          display: flex;
          align-items: flex-start;
          gap: 15px;
        }

        .task-header {
          display: flex;
          flex: 1;
          align-items: flex-start;
          gap: 12px;
        }

        .task-checkbox {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          border: 2px solid var(--text-muted);
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          flex-shrink: 0;
          transition: all 0.2s ease;
          font-weight: bold;
          margin-top: 4px;
        }

        .task-checkbox:hover {
          border-color: var(--primary-color);
          background-color: rgba(99, 102, 241, 0.1);
        }

        .task-checkbox.completed {
          background: linear-gradient(135deg, var(--success), #059669);
          border-color: var(--success);
          color: white;
        }

        .task-text {
          flex: 1;
        }

        .task-title-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 10px;
          margin-bottom: 6px;
        }

        .task-title {
          margin: 0;
          font-size: 1.2rem;
          font-weight: 600;
          color: var(--text-primary);
          flex: 1;
        }

        .task-title.completed {
          text-decoration: line-through;
          color: var(--text-muted);
        }

        .priority-badge {
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .priority-high {
          background-color: rgba(239, 68, 68, 0.15);
          color: #f87171;
        }

        .priority-medium {
          background-color: rgba(245, 158, 11, 0.15);
          color: #fbbf24;
        }

        .priority-low {
          background-color: rgba(16, 185, 129, 0.15);
          color: #34d399;
        }

        .task-description {
          margin: 8px 0 10px 0;
          color: var(--text-secondary);
          line-height: 1.5;
        }

        .task-description.completed {
          color: var(--text-muted);
        }

        .task-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-bottom: 10px;
          font-size: 0.9rem;
          color: var(--text-muted);
        }

        .task-due-date, .task-created {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          border-radius: 6px;
          background-color: rgba(59, 130, 246, 0.1);
          color: #93c5fd;
        }

        .task-due-date.completed, .task-created.completed {
          background-color: rgba(148, 163, 184, 0.1);
          color: var(--text-muted);
        }

        .status-badge {
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .status-done {
          background-color: rgba(16, 185, 129, 0.15);
          color: #34d399;
        }

        .status-in-progress {
          background-color: rgba(245, 158, 11, 0.15);
          color: #fbbf24;
        }

        .status-todo {
          background-color: rgba(59, 130, 246, 0.15);
          color: #93c5fd;
        }

        .task-completed-badge {
          background-color: rgba(16, 185, 129, 0.15);
          color: #34d399;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 0.8rem;
          font-weight: 600;
        }

        .task-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
        }

        .tag-badge {
          background-color: rgba(148, 163, 184, 0.1);
          color: var(--text-secondary);
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 0.8rem;
        }

        .task-actions {
          display: flex;
          gap: 8px;
          flex-shrink: 0;
        }

        .edit-btn, .delete-btn {
          border: none;
          background: none;
          cursor: pointer;
          font-size: 1.2rem;
          padding: 8px;
          border-radius: 8px;
          transition: background-color 0.2s;
          color: var(--text-secondary);
        }

        .edit-btn:hover {
          background-color: rgba(99, 102, 241, 0.1);
          color: var(--primary-color);
        }

        .delete-btn:hover {
          background-color: rgba(239, 68, 68, 0.1);
          color: #ef4444;
        }

        .edit-form {
          flex: 1;
        }

        .edit-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
        }

        .edit-title {
          flex: 1;
          padding: 12px 16px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          font-size: 1.1rem;
          font-weight: 600;
          color: var(--text-primary);
        }

        .edit-title:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .edit-description {
          width: 100%;
          padding: 12px 16px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          min-height: 80px;
          margin-bottom: 12px;
          resize: vertical;
          color: var(--text-primary);
          font-family: inherit;
        }

        .edit-description:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .edit-row {
          display: flex;
          gap: 12px;
          margin-bottom: 12px;
        }

        .edit-priority, .edit-date, .edit-status {
          padding: 10px 14px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          color: var(--text-primary);
        }

        .edit-priority, .edit-status {
          flex: 1;
        }

        .edit-date {
          flex: 1;
        }

        .edit-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
          margin-bottom: 12px;
        }

        .tag-chip {
          background-color: rgba(99, 102, 241, 0.15);
          color: var(--primary-color);
          padding: 4px 10px;
          border-radius: 20px;
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }

        .remove-tag-btn {
          background: none;
          border: none;
          font-size: 1.2rem;
          cursor: pointer;
          color: #ef4444;
          padding: 0 0 2px 4px;
        }

        .edit-buttons {
          display: flex;
          gap: 10px;
          justify-content: flex-end;
        }

        .save-btn, .cancel-btn {
          padding: 10px 20px;
          border: none;
          border-radius: var(--border-radius);
          cursor: pointer;
          font-weight: 500;
          transition: all 0.2s ease;
        }

        .save-btn {
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
        }

        .save-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .cancel-btn {
          background: rgba(148, 163, 184, 0.15);
          color: var(--text-secondary);
        }

        .cancel-btn:hover {
          background: rgba(148, 163, 184, 0.25);
        }

        @media (max-width: 768px) {
          .task-content {
            flex-direction: column;
            gap: 12px;
          }

          .task-header {
            width: 100%;
          }

          .task-actions {
            align-self: flex-start;
            margin-top: 10px;
          }

          .task-title-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
          }

          .task-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
          }

          .edit-row {
            flex-direction: column;
            gap: 12px;
          }

          .edit-title {
            font-size: 1rem;
          }
        }

        @media (max-width: 480px) {
          .task-item {
            padding: 16px;
          }

          .task-title {
            font-size: 1.1rem;
          }

          .edit-title {
            font-size: 0.95rem;
          }

          .edit-description {
            min-height: 60px;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoItem;