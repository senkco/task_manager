"""
Command-line interface for the Task Management Application.
"""
from task_manager import TaskManager
from database import DatabaseHandler
from task import Task
import sys


class TaskManagementCLI:
    """
    Command-line interface for interacting with the Task Management system.
    """
    
    def __init__(self):
        """Initialize the CLI with database and task manager."""
        try:
            self.db_handler = DatabaseHandler()
            self.db_handler.connect()
            self.task_manager = TaskManager(self.db_handler)
        except Exception as e:
            print(f"Error initializing application: {e}")
            sys.exit(1)
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("        TASK MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add a new task")
        print("2. List all tasks")
        print("3. Update a task")
        print("4. Mark task as completed")
        print("5. Delete a task")
        print("6. Filter tasks")
        print("7. Exit")
        print("="*50)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """
        Get user input with validation.
        
        Args:
            prompt: The prompt to display
            required: Whether the input is required
            
        Returns:
            User input string
        """
        while True:
            value = input(prompt).strip()
            if not required or value:
                return value
            print("This field is required. Please enter a value.")
    
    def add_task_flow(self):
        """Handle the add task workflow."""
        print("\n--- Add New Task ---")
        
        title = self.get_input("Enter task title: ")
        description = self.get_input("Enter task description: ", required=False)
        
        while True:
            due_date = self.get_input("Enter due date (YYYY-MM-DD): ")
            try:
                from datetime import datetime
                datetime.strptime(due_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        print("\nPriority levels: Low, Medium, High")
        while True:
            priority = self.get_input("Enter priority: ").capitalize()
            if priority in Task.VALID_PRIORITIES:
                break
            print(f"Invalid priority. Choose from: {', '.join(Task.VALID_PRIORITIES)}")
        
        task = self.task_manager.add_task(title, description, due_date, priority)
        if task:
            print(f"\n✓ Task added successfully!")
    
    def list_tasks_flow(self):
        """Handle the list tasks workflow."""
        print("\n--- List Tasks ---")
        print("1. List all tasks")
        print("2. Sort tasks")
        
        choice = self.get_input("Choose option (1-2): ")
        
        tasks = self.task_manager.get_all_tasks()
        
        if not tasks:
            print("\nNo tasks found.")
            return
        
        if choice == '2':
            print("\nSort by:")
            print("1. Due date")
            print("2. Priority")
            print("3. Creation date")
            
            sort_choice = self.get_input("Choose option (1-3): ")
            
            sort_map = {
                '1': 'due_date',
                '2': 'priority',
                '3': 'created_at'
            }
            
            sort_by = sort_map.get(sort_choice, 'due_date')
            tasks = self.task_manager.sort_tasks(tasks, sort_by=sort_by)
        
        self.display_tasks(tasks)
    
    def display_tasks(self, tasks):
        """
        Display a list of tasks in a formatted way.
        
        Args:
            tasks: List of Task objects to display
        """
        print(f"\n{'ID':<10} {'Title':<25} {'Due Date':<12} {'Priority':<10} {'Status':<15}")
        print("-" * 80)
        
        for task in tasks:
            print(f"{task.task_id:<10} {task.title[:24]:<25} {task.due_date:<12} "
                  f"{task.priority:<10} {task.status:<15}")
        
        print(f"\nTotal tasks: {len(tasks)}")
    
    def update_task_flow(self):
        """Handle the update task workflow."""
        print("\n--- Update Task ---")
        
        task_id = self.get_input("Enter task ID: ")
        
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID '{task_id}' not found.")
            return
        
        print(f"\nCurrent task details:")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Due Date: {task.due_date}")
        print(f"Priority: {task.priority}")
        print(f"Status: {task.status}")
        
        print("\nWhat would you like to update?")
        print("1. Title")
        print("2. Description")
        print("3. Due Date")
        print("4. Priority")
        print("5. Status")
        
        choice = self.get_input("Choose option (1-5): ")
        
        update_data = {}
        
        if choice == '1':
            new_title = self.get_input("Enter new title: ")
            update_data['title'] = new_title
        elif choice == '2':
            new_desc = self.get_input("Enter new description: ", required=False)
            update_data['description'] = new_desc
        elif choice == '3':
            while True:
                new_date = self.get_input("Enter new due date (YYYY-MM-DD): ")
                try:
                    from datetime import datetime
                    datetime.strptime(new_date, '%Y-%m-%d')
                    update_data['due_date'] = new_date
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD")
        elif choice == '4':
            print(f"Priority levels: {', '.join(Task.VALID_PRIORITIES)}")
            while True:
                new_priority = self.get_input("Enter new priority: ").capitalize()
                if new_priority in Task.VALID_PRIORITIES:
                    update_data['priority'] = new_priority
                    break
                print(f"Invalid priority.")
        elif choice == '5':
            print(f"Status options: {', '.join(Task.VALID_STATUSES)}")
            while True:
                new_status = self.get_input("Enter new status: ")
                # Handle common input variations
                if new_status.lower() == 'pending':
                    new_status = 'Pending'
                elif new_status.lower() in ['in progress', 'inprogress']:
                    new_status = 'In Progress'
                elif new_status.lower() == 'completed':
                    new_status = 'Completed'
                
                if new_status in Task.VALID_STATUSES:
                    update_data['status'] = new_status
                    break
                print(f"Invalid status.")
        
        if update_data:
            self.task_manager.update_task(task_id, **update_data)
    
    def mark_completed_flow(self):
        """Handle the mark completed workflow."""
        print("\n--- Mark Task as Completed ---")
        
        task_id = self.get_input("Enter task ID: ")
        
        if self.task_manager.mark_completed(task_id):
            print("✓ Task marked as completed!")
    
    def delete_task_flow(self):
        """Handle the delete task workflow."""
        print("\n--- Delete Task ---")
        
        task_id = self.get_input("Enter task ID: ")
        
        # Confirm deletion
        confirm = self.get_input(f"Are you sure you want to delete task '{task_id}'? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            if self.task_manager.delete_task(task_id):
                print("✓ Task deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    def filter_tasks_flow(self):
        """Handle the filter tasks workflow."""
        print("\n--- Filter Tasks ---")
        print("Filter by:")
        print("1. Priority")
        print("2. Status")
        print("3. Due Date")
        
        choice = self.get_input("Choose option (1-3): ")
        
        if choice == '1':
            print(f"Priority levels: {', '.join(Task.VALID_PRIORITIES)}")
            filter_value = self.get_input("Enter priority: ").capitalize()
            if filter_value not in Task.VALID_PRIORITIES:
                print("Invalid priority.")
                return
            tasks = self.task_manager.filter_tasks('priority', filter_value)
        elif choice == '2':
            print(f"Status options: {', '.join(Task.VALID_STATUSES)}")
            filter_value = self.get_input("Enter status: ")
            # Handle common variations
            if filter_value.lower() == 'pending':
                filter_value = 'Pending'
            elif filter_value.lower() in ['in progress', 'inprogress']:
                filter_value = 'In Progress'
            elif filter_value.lower() == 'completed':
                filter_value = 'Completed'
            
            if filter_value not in Task.VALID_STATUSES:
                print("Invalid status.")
                return
            tasks = self.task_manager.filter_tasks('status', filter_value)
        elif choice == '3':
            filter_value = self.get_input("Enter due date (YYYY-MM-DD): ")
            tasks = self.task_manager.filter_tasks('due_date', filter_value)
        else:
            print("Invalid choice.")
            return
        
        if tasks:
            self.display_tasks(tasks)
        else:
            print("\nNo tasks found matching the filter criteria.")
    
    def run(self):
        """Main application loop."""
        print("\nWelcome to Task Management System!")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_input("\nEnter your choice (1-7): ")
                
                if choice == '1':
                    self.add_task_flow()
                elif choice == '2':
                    self.list_tasks_flow()
                elif choice == '3':
                    self.update_task_flow()
                elif choice == '4':
                    self.mark_completed_flow()
                elif choice == '5':
                    self.delete_task_flow()
                elif choice == '6':
                    self.filter_tasks_flow()
                elif choice == '7':
                    print("\nThank you for using Task Management System!")
                    self.db_handler.disconnect()
                    break
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 7.")
                    
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Exiting...")
                self.db_handler.disconnect()
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")


if __name__ == "__main__":
    app = TaskManagementCLI()
    app.run()