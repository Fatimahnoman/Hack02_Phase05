import React, { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';
import TodoForm from '../components/todos/TodoForm';
import TodoList from '../components/todos/TodoList';
import { Todo, TodoCreate, TodoUpdate } from '../types';
import { todoAPI } from '../services/api';
import { useRouter } from 'next/router';

const DashboardPage = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await todoAPI.getAll();
        setTodos(response.data);
      } catch (error) {
        console.error('Error fetching todos:', error);
        // Redirect to sign in if unauthorized
        if ((error as any).response?.status === 401) {
          router.push('/signin');
        }
      } finally {
        setLoading(false);
      }
    };

    // Check if user is authenticated before fetching todos
    if (localStorage.getItem('access_token')) {
      fetchTodos();
    } else {
      router.push('/signin');
    }
  }, [router]);

  const handleAddTodo = async (todoData: TodoCreate) => {
    try {
      const response = await todoAPI.create(todoData);
      setTodos([...todos, response.data]);
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  const handleToggleTodo = async (id: number, completed: boolean) => {
    try {
      const response = await todoAPI.toggleComplete(id, completed);
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed: response.data.completed } : todo
      ));
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const handleUpdateTodo = async (id: number, updates: TodoUpdate) => {
    try {
      const response = await todoAPI.update(id, updates);
      setTodos(todos.map(todo =>
        todo.id === id ? response.data : todo
      ));
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await todoAPI.delete(id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="container">
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container">
        <h1>My Todo List</h1>
        <TodoForm onSubmit={handleAddTodo} />
        <TodoList
          todos={todos}
          onToggle={handleToggleTodo}
          onUpdate={handleUpdateTodo}
          onDelete={handleDeleteTodo}
          emptyState={<div className="empty-state">No todos yet. Add one to get started!</div>}
        />
      </div>
    </Layout>
  );
};

export default DashboardPage;