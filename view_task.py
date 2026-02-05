import sqlite3
from datetime import datetime

def view_all_tasks():
      # Connect to the database
      conn = sqlite3.connect('backend/chat_app.db')
      cursor = conn.cursor()

      print("🔍 AI-MANAGED TASKS (Created via Chatbot)")
      print("="*60)
      cursor.execute('SELECT * FROM task ORDER BY created_at DESC;')
      tasks = cursor.fetchall()

      if tasks:
          for task in tasks:
              print(f"ID: {task[0]}")
              print(f"Title: {task[1]}")
              print(f"Description: {task[2]}")
              print(f"Status: {task[3]}")
              print(f"Priority: {task[4]}")
              print(f"Created: {task[5]}")
              print(f"Updated: {task[6]}")
              print(f"Completed: {task[7] if task[7] else 'Not completed'}")
              print("-" * 40)
      else:
          print("No AI-managed tasks found.")

      print("\n📋 TRADITIONAL TODOS (Created via UI)")
      print("="*60)
      cursor.execute('SELECT * FROM todo ORDER BY created_at DESC;')
      todos = cursor.fetchall()

      if todos:
          for todo in todos:
              print(f"ID: #{todo[0]}")
              print(f"Title: {todo[1]}")
              print(f"Description: {todo[2] or 'No description'}")
              print(f"Completed: {'Yes' if todo[3] else 'No'}")
              print(f"Due Date: {todo[4] or 'No due date'}")
              print(f"User ID: {todo[5]}")
              print(f"Created: {todo[6]}")
              print(f"Updated: {todo[7]}")
              print("-" * 40)
      else:
          print("No traditional todos found.")

      conn.close()

if __name__ == "__main__":
      view_all_tasks()

