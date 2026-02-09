from datetime import datetime
from typing import Optional


class Task:
    """
    Represents a task with all its attributes.
    
    Attributes:
        task_id (str): Unique identifier for the task
        title (str): Title of the task
        description (str): Detailed description
        due_date (str): Due date in YYYY-MM-DD format
        priority (str): Priority level (Low, Medium, High)
        status (str): Current status (Pending, In Progress, Completed)
        created_at (str): Creation timestamp
    """
    
    VALID_PRIORITIES = ['Low', 'Medium', 'High']
    VALID_STATUSES = ['Pending', 'In Progress', 'Completed']
    
    def __init__(self, task_id: str, title: str, description: str, 
                 due_date: str, priority: str, status: str = 'Pending',
                 created_at: Optional[str] = None):
        """
        Initialize a new Task instance.
        
        Args:
            task_id: Unique identifier for the task
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level (Low, Medium, High)
            status: Task status (default: Pending)
            created_at: Creation timestamp (default: current time)
        """
        self._task_id = task_id
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority
        self._status = status
        self._created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Getters
    @property
    def task_id(self) -> str:
        return self._task_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def due_date(self) -> str:
        return self._due_date
    
    @property
    def priority(self) -> str:
        return self._priority
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    # Setters with validation
    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @description.setter
    def description(self, value: str):
        self._description = value.strip()
    
    @due_date.setter
    def due_date(self, value: str):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            self._due_date = value
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
    
    @priority.setter
    def priority(self, value: str):
        if value not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}")
        self._priority = value
    
    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value
    
    def to_dict(self) -> dict:
        """Convert task to dictionary format for database storage."""
        return {
            'task_id': self._task_id,
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date,
            'priority': self._priority,
            'status': self._status,
            'created_at': self._created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(
            task_id=data['task_id'],
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            priority=data['priority'],
            status=data['status'],
            created_at=data['created_at']
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        return (f"[{self._task_id}] {self._title} | "
                f"Due: {self._due_date} | Priority: {self._priority} | "
                f"Status: {self._status}")
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"Task(task_id='{self._task_id}', title='{self._title}')"


