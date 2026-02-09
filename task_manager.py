"""
TaskManager class for managing tasks with sorting and filtering capabilities.
"""
from typing import List, Optional, Callable
from datetime import datetime
from task import Task
from database import DatabaseHandler
import uuid


class TaskManager:
    """
    Manages tasks including CRUD operations, sorting, and filtering.
    """
    
    def __init__(self, db_handler: DatabaseHandler):
        """
        Initialize TaskManager with a database handler.
        
        Args:
            db_handler: DatabaseHandler instance for persistence
        """
        self._db_handler = db_handler
        self._tasks = {}  # In-memory cache: {task_id: Task}
        self._load_tasks_from_db()
    
    def _load_tasks_from_db(self):
        """Load all tasks from database into memory."""
        try:
            tasks_data = self._db_handler.get_all_tasks()
            for task_data in tasks_data:
                task = Task.from_dict(task_data)
                self._tasks[task.task_id] = task
            print(f"Loaded {len(self._tasks)} tasks from database")
        except Exception as e:
            print(f"Error loading tasks from database: {e}")
    
    def _generate_task_id(self) -> str:
        """Generate a unique task ID."""
        return str(uuid.uuid4())[:8]
    
    def add_task(self, title: str, description: str, due_date: str, 
                 priority: str) -> Optional[Task]:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level (Low, Medium, High)
            
        Returns:
            The created Task object or None if failed
        """
        try:
            # Validate inputs
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            
            if priority not in Task.VALID_PRIORITIES:
                raise ValueError(f"Invalid priority. Choose from: {', '.join(Task.VALID_PRIORITIES)}")
            
            # Validate date format
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")
            
            # Generate unique ID
            task_id = self._generate_task_id()
            while task_id in self._tasks:
                task_id = self._generate_task_id()
            
            # Create task
            task = Task(task_id, title, description, due_date, priority)
            
            # Save to database
            if self._db_handler.insert_task(task.to_dict()):
                self._tasks[task_id] = task
                print(f"Task '{title}' added successfully with ID: {task_id}")
                return task
            else:
                print("Failed to save task to database")
                return None
                
        except ValueError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all Task objects
        """
        return list(self._tasks.values())
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: The task identifier
            
        Returns:
            Task object or None if not found
        """
        return self._tasks.get(task_id)
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """
        Update a task's details.
        
        Args:
            task_id: The task identifier
            **kwargs: Fields to update (title, description, due_date, priority, status)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            task = self._tasks.get(task_id)
            if not task:
                print(f"Task with ID '{task_id}' not found")
                return False
            
            # Update allowed fields
            update_data = {}
            
            if 'title' in kwargs:
                task.title = kwargs['title']
                update_data['title'] = kwargs['title']
            
            if 'description' in kwargs:
                task.description = kwargs['description']
                update_data['description'] = kwargs['description']
            
            if 'due_date' in kwargs:
                task.due_date = kwargs['due_date']
                update_data['due_date'] = kwargs['due_date']
            
            if 'priority' in kwargs:
                task.priority = kwargs['priority']
                update_data['priority'] = kwargs['priority']
            
            if 'status' in kwargs:
                task.status = kwargs['status']
                update_data['status'] = kwargs['status']
            
            if update_data:
                if self._db_handler.update_task(task_id, update_data):
                    print(f"Task '{task_id}' updated successfully")
                    return True
                else:
                    print("Failed to update task in database")
                    return False
            else:
                print("No fields to update")
                return False
                
        except ValueError as e:
            print(f"Validation error: {e}")
            return False
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def mark_completed(self, task_id: str) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The task identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.update_task(task_id, status='Completed')
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if task_id not in self._tasks:
                print(f"Task with ID '{task_id}' not found")
                return False
            
            if self._db_handler.delete_task(task_id):
                del self._tasks[task_id]
                print(f"Task '{task_id}' deleted successfully")
                return True
            else:
                print("Failed to delete task from database")
                return False
                
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def filter_tasks(self, filter_by: str = None, filter_value: str = None) -> List[Task]:
        """
        Filter tasks based on criteria.
        
        Args:
            filter_by: Field to filter by (priority, status, due_date)
            filter_value: Value to filter for
            
        Returns:
            List of filtered Task objects
        """
        tasks = self.get_all_tasks()
        
        if not filter_by or not filter_value:
            return tasks
        
        filtered_tasks = []
        
        for task in tasks:
            if filter_by == 'priority' and task.priority == filter_value:
                filtered_tasks.append(task)
            elif filter_by == 'status' and task.status == filter_value:
                filtered_tasks.append(task)
            elif filter_by == 'due_date' and task.due_date == filter_value:
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def sort_tasks(self, tasks: List[Task], sort_by: str = 'due_date', 
                   reverse: bool = False) -> List[Task]:
        """
        Sort tasks using a custom sorting algorithm (insertion sort).
        
        Args:
            tasks: List of tasks to sort
            sort_by: Field to sort by (due_date, priority, created_at)
            reverse: Sort in descending order if True
            
        Returns:
            Sorted list of Task objects
        """
        if not tasks:
            return []
        
        # Create a copy to avoid modifying original list
        sorted_tasks = tasks.copy()
        
        # Define comparison keys
        priority_order = {'Low': 1, 'Medium': 2, 'High': 3}
        
        # Insertion sort implementation
        for i in range(1, len(sorted_tasks)):
            key_task = sorted_tasks[i]
            j = i - 1
            
            # Get comparison values
            if sort_by == 'priority':
                key_value = priority_order.get(key_task.priority, 0)
            elif sort_by == 'created_at':
                key_value = key_task.created_at
            else:  # default to due_date
                key_value = key_task.due_date
            
            # Move elements greater than key to one position ahead
            while j >= 0:
                if sort_by == 'priority':
                    compare_value = priority_order.get(sorted_tasks[j].priority, 0)
                elif sort_by == 'created_at':
                    compare_value = sorted_tasks[j].created_at
                else:
                    compare_value = sorted_tasks[j].due_date
                
                if (not reverse and compare_value > key_value) or \
                   (reverse and compare_value < key_value):
                    sorted_tasks[j + 1] = sorted_tasks[j]
                    j -= 1
                else:
                    break
            
            sorted_tasks[j + 1] = key_task
        
        return sorted_tasks