import React, { useState, useEffect } from 'react';
import { TaskCreate } from '../../types';
import { tagAPI } from '../../services/api';

interface TaskFormProps {
  onSubmit: (task: TaskCreate) => void;
}

const TodoForm = ({ onSubmit }: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [reminderOffset, setReminderOffset] = useState<number>(60); // Default to 1 hour before
  const [tags, setTags] = useState<string[]>([]);
  const [newTag, setNewTag] = useState('');
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [recurringType, setRecurringType] = useState<'none' | 'daily' | 'weekly' | 'monthly' | 'custom'>('none');
  const [recurringInterval, setRecurringInterval] = useState<number>(1);
  const [recurringStartDate, setRecurringStartDate] = useState('');
  const [recurringEndDate, setRecurringEndDate] = useState('');

  // Load available tags
  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await tagAPI.getAll();
        const tagNames = response.data.tags.map(tag => tag.name);
        setAvailableTags(tagNames);
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };
    fetchTags();
  }, []);

  const handleAddTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      if (tags.length < 5) { // Max 5 tags
        setTags([...tags, newTag.trim()]);
        setNewTag('');
      } else {
        alert('Maximum 5 tags allowed per task');
      }
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    // Format the date to ISO string if provided
    let formattedDueDate: string | undefined = undefined;
    if (dueDate) {
      const date = new Date(dueDate);
      formattedDueDate = date.toISOString();
    }

    // Format recurring pattern if selected
    let recurringPattern = undefined;
    if (recurringType !== 'none') {
      recurringPattern = {
        recurrence_type: recurringType,
        interval: recurringInterval,
        start_date: recurringStartDate ? new Date(recurringStartDate).toISOString() : new Date().toISOString(),
        end_date: recurringEndDate ? new Date(recurringEndDate).toISOString() : undefined,
      };
    }

    const taskData: TaskCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      due_date: formattedDueDate,
      reminder_offset: dueDate ? reminderOffset : undefined, // Only set if due date exists
      tags,
      recurring_pattern: recurringPattern
    };

    onSubmit(taskData);
    
    // Reset form
    setTitle('');
    setDescription('');
    setPriority('medium');
    setDueDate('');
    setReminderOffset(60);
    setTags([]);
    setRecurringType('none');
    setRecurringInterval(1);
    setRecurringStartDate('');
    setRecurringEndDate('');
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <div className="form-header">
        <h2>Add New Task</h2>
        <p className="form-subtitle">Create a new task with advanced features</p>
      </div>

      <div className="form-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          className="title-input"
          required
        />
      </div>
      
      <div className="form-group">
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description (optional)"
          className="description-input"
        />
      </div>
      
      <div className="form-row">
        <div className="form-group">
          <label className="priority-label">Priority</label>
          <select 
            value={priority} 
            onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
            className="priority-select"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        
        <div className="form-group">
          <label className="date-label">Due Date</label>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="date-input"
          />
        </div>
      </div>
      
      {dueDate && (
        <div className="form-group">
          <label className="reminder-label">Reminder Offset (minutes before due date)</label>
          <input
            type="number"
            value={reminderOffset}
            onChange={(e) => setReminderOffset(Number(e.target.value))}
            className="reminder-input"
            min="1"
            max="43200" // Max 30 days in minutes
          />
        </div>
      )}
      
      <div className="form-group">
        <label className="tags-label">Tags (max 5)</label>
        <div className="tags-input-container">
          <div className="tags-list">
            {tags.map((tag, index) => (
              <span key={index} className="tag-chip">
                #{tag}
                <button 
                  type="button" 
                  onClick={() => handleRemoveTag(tag)}
                  className="remove-tag-btn"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
          <div className="tag-input-row">
            <input
              type="text"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="Add a tag..."
              className="tag-input"
              list="available-tags"
            />
            <datalist id="available-tags">
              {availableTags
                .filter(tag => !tags.includes(tag))
                .map((tag, index) => (
                  <option key={index} value={tag} />
                ))}
            </datalist>
            <button 
              type="button" 
              onClick={handleAddTag}
              className="add-tag-btn"
              disabled={!newTag.trim() || tags.length >= 5}
            >
              Add
            </button>
          </div>
        </div>
      </div>
      
      <div className="form-group">
        <label className="recurring-label">Recurring Pattern</label>
        <select 
          value={recurringType} 
          onChange={(e) => setRecurringType(e.target.value as any)}
          className="recurring-select"
        >
          <option value="none">Not recurring</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="custom">Custom</option>
        </select>
        
        {recurringType !== 'none' && (
          <div className="recurring-details">
            <div className="form-row">
              <div className="form-group">
                <label>Interval</label>
                <input
                  type="number"
                  value={recurringInterval}
                  onChange={(e) => setRecurringInterval(Math.max(1, Number(e.target.value)))}
                  className="interval-input"
                  min="1"
                />
              </div>
              
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  value={recurringStartDate}
                  onChange={(e) => setRecurringStartDate(e.target.value)}
                  className="date-input"
                />
              </div>
            </div>
            
            <div className="form-group">
              <label>End Date (optional)</label>
              <input
                type="date"
                value={recurringEndDate}
                onChange={(e) => setRecurringEndDate(e.target.value)}
                className="date-input"
              />
            </div>
          </div>
        )}
      </div>
      
      <button type="submit" className="submit-btn btn-primary">Add Task</button>
      
      <style jsx>{`
        .task-form {
          background: var(--card-bg);
          border-radius: var(--border-radius);
          padding: 30px;
          margin-bottom: 30px;
          border: 1px solid var(--card-border);
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .form-header {
          margin-bottom: 25px;
          text-align: center;
        }

        .form-header h2 {
          margin: 0 0 8px 0;
          font-size: 1.6rem;
          font-weight: 700;
          color: var(--text-primary);
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .form-subtitle {
          margin: 0;
          color: var(--text-secondary);
          font-size: 1rem;
          font-weight: 500;
        }

        .form-group {
          margin-bottom: 20px;
        }

        .form-row {
          display: flex;
          gap: 15px;
        }

        .form-row .form-group {
          flex: 1;
        }

        .priority-label, .date-label, .reminder-label, .tags-label, .recurring-label {
          display: block;
          margin-bottom: 10px;
          font-weight: 600;
          color: var(--text-secondary);
          font-size: 1rem;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .title-input, .description-input, .date-input, .reminder-input, .tag-input, .priority-select, .recurring-select, .interval-input {
          width: 100%;
          padding: 14px 18px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          font-size: 1.05rem;
          transition: all 0.3s ease;
          color: var(--text-primary);
        }

        .title-input:focus, .description-input:focus, .date-input:focus, .reminder-input:focus, .tag-input:focus, .priority-select:focus, .recurring-select:focus, .interval-input:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .description-input {
          height: 120px;
          resize: vertical;
          font-family: inherit;
          line-height: 1.5;
          background: rgba(30, 41, 59, 0.5);
          color: var(--text-primary);
        }

        .tags-input-container {
          width: 100%;
        }

        .tags-list {
          min-height: 40px;
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius) var(--border-radius) 0 0;
          padding: 8px;
          background: rgba(30, 41, 59, 0.5);
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .tag-chip {
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          padding: 4px 8px;
          border-radius: 20px;
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }

        .remove-tag-btn {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          font-weight: bold;
          padding: 0 0 2px 4px;
        }

        .tag-input-row {
          display: flex;
          border: 1px solid var(--card-border);
          border-top: none;
          border-radius: 0 0 var(--border-radius) var(--border-radius);
        }

        .tag-input {
          flex: 1;
          border: none;
          padding: 12px 18px;
          border-radius: 0 0 0 var(--border-radius);
          background: rgba(30, 41, 59, 0.5);
          color: var(--text-primary);
        }

        .tag-input:focus {
          outline: none;
        }

        .add-tag-btn {
          border: none;
          border-radius: 0 0 var(--border-radius) 0;
          padding: 0 18px;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          cursor: pointer;
        }

        .add-tag-btn:disabled {
          background: rgba(148, 163, 184, 0.3);
          cursor: not-allowed;
        }

        .recurring-details {
          margin-top: 15px;
          padding: 15px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
        }

        .submit-btn {
          width: 100%;
          padding: 16px;
          border: none;
          border-radius: var(--border-radius);
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          letter-spacing: 0.5px;
          box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .submit-btn:hover {
          transform: translateY(-3px);
          box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }

        .submit-btn:active {
          transform: translateY(0);
          box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        @media (max-width: 768px) {
          .task-form {
            padding: 25px 20px;
          }

          .form-header h2 {
            font-size: 1.4rem;
          }

          .form-subtitle {
            font-size: 0.95rem;
          }

          .form-row {
            flex-direction: column;
            gap: 15px;
          }

          .form-row .form-group {
            flex: none;
          }

          .title-input, .description-input, .date-input, .reminder-input, .tag-input, .priority-select, .recurring-select, .interval-input {
            padding: 12px 16px;
            font-size: 1rem;
          }

          .recurring-details {
            padding: 12px;
          }
        }

        @media (max-width: 480px) {
          .task-form {
            padding: 20px 15px;
          }

          .form-header {
            margin-bottom: 20px;
          }

          .form-header h2 {
            font-size: 1.3rem;
          }

          .form-group {
            margin-bottom: 16px;
          }

          .priority-label, .date-label, .reminder-label, .tags-label, .recurring-label {
            font-size: 0.9rem;
          }

          .submit-btn {
            padding: 14px;
            font-size: 1rem;
          }
        }
      `}</style>
    </form>
  );
};

export default TodoForm;