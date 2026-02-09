"""
Database handler for MongoDB operations.
"""
from typing import List, Optional, Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError


class DatabaseHandler:
    """
    Handles all database operations for the Task Management Application.
    Uses MongoDB for data persistence.
    """
    
    def __init__(self, connection_string: str = 'mongodb://localhost:27017/',
                 database_name: str = 'task_management'):
        """
        Initialize database connection.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self._connection_string = connection_string
        self._database_name = database_name
        self._client = None
        self._db = None
        self._collection = None
        
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            self._client = MongoClient(self._connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[self._database_name]
            self._collection = self._db['tasks']
            print("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error during connection: {e}")
    
    def disconnect(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            print("Database connection closed")
    
    def insert_task(self, task_data: Dict[str, Any]) -> bool:
        """
        Insert a new task into the database.
        
        Args:
            task_data: Dictionary containing task information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._collection.insert_one(task_data)
            return True
        except PyMongoError as e:
            print(f"Error inserting task: {e}")
            return False
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks from the database.
        
        Returns:
            List of task dictionaries
        """
        try:
            tasks = list(self._collection.find({}, {'_id': 0}))
            return tasks
        except PyMongoError as e:
            print(f"Error retrieving tasks: {e}")
            return []
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific task by ID.
        
        Args:
            task_id: The unique task identifier
            
        Returns:
            Task dictionary or None if not found
        """
        try:
            task = self._collection.find_one({'task_id': task_id}, {'_id': 0})
            return task
        except PyMongoError as e:
            print(f"Error retrieving task: {e}")
            return None
    
    def update_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a task in the database.
        
        Args:
            task_id: The unique task identifier
            update_data: Dictionary containing fields to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self._collection.update_one(
                {'task_id': task_id},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating task: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the database.
        
        Args:
            task_id: The unique task identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self._collection.delete_one({'task_id': task_id})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting task: {e}")
            return False
    
    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task exists in the database.
        
        Args:
            task_id: The unique task identifier
            
        Returns:
            bool: True if task exists, False otherwise
        """
        try:
            count = self._collection.count_documents({'task_id': task_id})
            return count > 0
        except PyMongoError as e:
            print(f"Error checking task existence: {e}")
            return False