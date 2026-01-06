import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import TodoItem from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: number, completed: boolean) => void;
  onUpdate: (id: number, updates: TodoUpdate) => void;
  onDelete: (id: number) => void;
  emptyState?: React.ReactNode;
}

const TodoList = ({ todos, onToggle, onUpdate, onDelete, emptyState }: TodoListProps) => {
  if (todos.length === 0) {
    return emptyState || <div className="empty-state">No todos yet. Add one to get started!</div>;
  }

  return (
    <div className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
      <style jsx>{`
        .todo-list {
          display: flex;
          flex-direction: column;
        }

        .empty-state {
          text-align: center;
          padding: 40px 20px;
          color: #888;
          font-style: italic;
        }

        @media (max-width: 768px) {
          .todo-list {
            margin: 0 10px;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoList;