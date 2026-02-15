import React, { useState, useEffect } from 'react';
import TaskForm from '../components/todos/TodoForm'; // Using updated TodoForm as TaskForm
import TodoList from '../components/todos/TodoList';
import { Todo, TodoCreate, TodoUpdate, TaskCreate } from '../types';
import { todoAPI, taskAPI, Task } from '../services/api';
import { useRouter } from 'next/router';

const DashboardPage = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<boolean>(false);
  const [showAddForm, setShowAddForm] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated before accessing dashboard
    if (!localStorage.getItem('access_token')) {
      alert('Signin First then you\'ll able to see the Dashboard');
      router.push('/signin');
      return;
    }

    const fetchData = async () => {
      try {
        // Fetch traditional todos
        try {
          const todosResponse = await todoAPI.getAll();
          setTodos(Array.isArray(todosResponse.data) ? todosResponse.data : []);
        } catch (error) {
          console.error('Error fetching todos:', error);
          // Don't fail completely if one fails
        }

        // Fetch AI-managed tasks
        try {
          const tasksResponse = await taskAPI.getAll();
          setTasks(Array.isArray(tasksResponse.data) ? tasksResponse.data : []);
        } catch (error) {
          console.error('Error fetching tasks:', error);
          // Don't fail completely if one fails
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Redirect to sign in if unauthorized
        if ((error as any).response?.status === 401) {
          alert('Signin First then you\'ll able to see the Dashboard');
          router.push('/signin');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [router]);

  const handleAddTask = async (taskData: TaskCreate) => {
    try {
      const response = await taskAPI.create(taskData);
      setTasks([...tasks, response.data]);
      setViewMode(false); // Reset view mode to show the form again
      setShowAddForm(false); // Hide the form after adding
      setSuccessMessage('Task Added Successfully in Task List');
      // Clear the message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      console.error('Error creating task:', error);
      // Show error message to user
      if (error instanceof Error) {
        alert(`Failed to add task: ${error.message}`);
      } else {
        alert('Failed to add task: Unknown error occurred');
      }
    }
  };

  const handleToggleTodo = async (id: number | string, completed: boolean) => {
    // Check if the ID is a string (meaning it's a task) or number (meaning it's a todo)
    if (typeof id === 'string') {
      // It's a task, handle with taskAPI
      try {
        const response = await taskAPI.updateStatus(id, completed);
        setTasks(tasks.map(task =>
          task.id === id ? response.data : task
        ));
        setSuccessMessage('Task Marked as Complete Successfully');
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error toggling task:', error);
        if (error instanceof Error) {
          alert(`Failed to update task status: ${error.message}`);
        } else {
          alert('Failed to update task status: Unknown error occurred');
        }
      }
    } else {
      // It's a todo, handle with todoAPI
      try {
        const response = await todoAPI.toggleComplete(id, completed);
        setTodos(todos.map(todo =>
          todo.id === id ? { ...todo, completed: response.data.completed } : todo
        ));
        const message = completed
          ? 'Task Marked as Complete Successfully'
          : 'Task Marked as Incomplete Successfully';
        setSuccessMessage(message);
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error toggling todo:', error);
        // Show error message to user
        if (error instanceof Error) {
          alert(`Failed to update task status: ${error.message}`);
        } else {
          alert('Failed to update task status: Unknown error occurred');
        }
      }
    }
  };

  const handleUpdateTodo = async (id: number | string, updates: TodoUpdate) => {
    // Check if the ID is a string (meaning it's a task) or number (meaning it's a todo)
    if (typeof id === 'string') {
      // It's a task, handle with taskAPI
      try {
        const response = await taskAPI.update(id, updates);
        setTasks(tasks.map(task =>
          task.id === id ? response.data : task
        ));
        setViewMode(false); // Reset view mode to show the form again
        setShowAddForm(false); // Hide the form if it was shown
        setSuccessMessage('Task Updated Successfully');
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error updating task:', error);
        if (error instanceof Error) {
          alert(`Failed to update task: ${error.message}`);
        } else {
          alert('Failed to update task: Unknown error occurred');
        }
      }
    } else {
      // It's a todo, handle with todoAPI
      try {
        const response = await todoAPI.update(id, updates);
        setTodos(todos.map(todo =>
          todo.id === id ? response.data : todo
        ));
        setViewMode(false); // Reset view mode to show the form again
        setShowAddForm(false); // Hide the form if it was shown
        setSuccessMessage('Task Updated Successfully in Todo List');
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error updating todo:', error);
        // Show error message to user
        if (error instanceof Error) {
          alert(`Failed to update task: ${error.message}`);
        } else {
          alert('Failed to update task: Unknown error occurred');
        }
      }
    }
  };

  const handleDeleteTodo = async (id: number | string) => {
    // Check if the ID is a string (meaning it's a task) or number (meaning it's a todo)
    if (typeof id === 'string') {
      // It's a task, handle with taskAPI
      try {
        await taskAPI.delete(id);
        setTasks(tasks.filter(task => task.id !== id));
        setViewMode(false); // Reset view mode to show the form again
        setShowAddForm(false); // Hide the form if it was shown
        setSuccessMessage('Task Deleted Successfully');
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error deleting task:', error);
        if (error instanceof Error) {
          alert(`Failed to delete task: ${error.message}`);
        } else {
          alert('Failed to delete task: Unknown error occurred');
        }
      }
    } else {
      // It's a todo, handle with todoAPI
      try {
        await todoAPI.delete(id);
        setTodos(todos.filter(todo => todo.id !== id));
        setViewMode(false); // Reset view mode to show the form again
        setShowAddForm(false); // Hide the form if it was shown
        setSuccessMessage('Task Deleted Successfully from Todo List');
        // Clear the message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } catch (error) {
        console.error('Error deleting todo:', error);
        // Show error message to user
        if (error instanceof Error) {
          alert(`Failed to delete task: ${error.message}`);
        } else {
          alert('Failed to delete task: Unknown error occurred');
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Double check authentication before rendering content
  if (!localStorage.getItem('access_token')) {
    // Show message and redirect
    if (typeof window !== 'undefined') {
      alert('Signin First then you\'ll able to see the Dashboard');
      window.location.href = '/signin';
    }

    return (
      <div className="dashboard-container">
        <p>Redirecting to sign in...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">Manage your tasks and boost productivity</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn-primary"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            {showAddForm ? 'Cancel' : '+ Add Task'}
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <h3>{todos.length + tasks.length}</h3>
            <p>Total Tasks</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{[...todos, ...tasks].filter(item => item.completed || item.status === 'done').length}</h3>
            <p>Completed</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <h3>{[...todos, ...tasks].filter(item => !item.completed && item.status !== 'done').length}</h3>
            <p>Pending</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>{Math.round(([...todos, ...tasks].filter(item => item.completed || item.status === 'done').length / Math.max(1, [...todos, ...tasks].length)) * 100)}%</h3>
            <p>Progress</p>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Conditionally render TaskForm based on showAddForm state */}
        {showAddForm && <TaskForm onSubmit={handleAddTask} />}

        <TodoList
          todos={[
            ...todos.map(todo => ({
              ...todo,
              type: 'todo' as const,
              originalId: todo.id
            })),
            ...tasks.map(task => ({
              id: parseInt(task.id) || 0, // Convert string ID to number for compatibility
              title: task.title,
              description: task.description || '',
              completed: task.status === 'done',
              created_at: task.created_at,
              updated_at: task.updated_at,
              user_id: 0, // Placeholder for compatibility
              type: 'task' as const,
              originalId: task.id
            }))
          ]}
          onToggle={handleToggleTodo}
          onUpdate={handleUpdateTodo}
          onDelete={handleDeleteTodo}
          emptyState={
            <div className="empty-state">
              <div className="empty-state-content">
                <div className="empty-state-icon">📋</div>
                <h3>No tasks yet</h3>
                <p>Add a new task to get started organizing your work</p>
                <button 
                  className="btn-primary"
                  onClick={() => setShowAddForm(true)}
                >
                  Add Your First Task
                </button>
              </div>
            </div>
          }
        />
      </div>

      {/* Success message display */}
      {successMessage && (
        <div className="success-toast">
          {successMessage}
        </div>
      )}

      <style jsx>{`
        .dashboard-container {
          width: 100%;
          padding: 0;
        }

        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 1px solid var(--card-border);
        }

        .header-content {
          flex: 1;
        }

        .dashboard-title {
          font-size: 28px;
          font-weight: 700;
          margin: 0 0 8px 0;
          color: var(--text-primary);
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .dashboard-subtitle {
          margin: 0;
          color: var(--text-secondary);
          font-size: 16px;
        }

        .header-actions {
          display: flex;
          gap: 12px;
        }

        .btn-primary {
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: var(--border-radius);
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 20px;
          margin-bottom: 30px;
        }

        .stat-card {
          background: var(--card-bg);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          padding: 24px;
          display: flex;
          align-items: center;
          gap: 16px;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .stat-icon {
          font-size: 32px;
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(99, 102, 241, 0.1);
          border-radius: 16px;
        }

        .stat-content h3 {
          margin: 0 0 4px 0;
          font-size: 28px;
          font-weight: 700;
          color: var(--text-primary);
        }

        .stat-content p {
          margin: 0;
          color: var(--text-secondary);
          font-size: 15px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .dashboard-content {
          background: var(--card-bg);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          padding: 25px;
          min-height: 500px;
        }

        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 400px;
          padding: 40px 20px;
        }

        .empty-state-content {
          text-align: center;
          max-width: 400px;
        }

        .empty-state-icon {
          font-size: 64px;
          margin-bottom: 20px;
        }

        .empty-state h3 {
          margin: 0 0 12px 0;
          font-size: 24px;
          font-weight: 700;
          color: var(--text-primary);
        }

        .empty-state p {
          margin: 0 0 24px 0;
          font-size: 16px;
          color: var(--text-secondary);
        }

        .success-toast {
          position: fixed;
          bottom: 20px;
          right: 20px;
          background: linear-gradient(135deg, var(--success), #059669);
          color: white;
          padding: 16px 24px;
          border-radius: var(--border-radius);
          box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
          z-index: 1000;
          animation: slideInFromRight 0.4s ease;
        }

        @keyframes slideInFromRight {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        .loading-spinner {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 500px;
        }

        .spinner {
          width: 50px;
          height: 50px;
          border: 5px solid rgba(99, 102, 241, 0.2);
          border-top: 5px solid var(--primary-color);
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 20px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
          .dashboard-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 16px;
          }

          .header-content {
            width: 100%;
          }

          .header-actions {
            width: 100%;
            justify-content: flex-end;
          }

          .stats-grid {
            grid-template-columns: 1fr;
            gap: 15px;
          }

          .dashboard-content {
            padding: 20px 15px;
          }

          .btn-primary {
            padding: 10px 20px;
            font-size: 0.95rem;
          }
        }

        @media (max-width: 480px) {
          .dashboard-header {
            gap: 12px;
          }

          .dashboard-title {
            font-size: 24px;
          }

          .stat-card {
            padding: 20px;
          }

          .stat-content h3 {
            font-size: 24px;
          }

          .empty-state-content {
            padding: 0 10px;
          }

          .empty-state-icon {
            font-size: 48px;
          }
        }
      `}</style>
    </div>
  );
};

export default DashboardPage;