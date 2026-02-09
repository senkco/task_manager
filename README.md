# Task Management Application

A command-line task management application built with Python and MongoDB, demonstrating OOP principles, custom algorithms, and database interaction.

## Features

- ✅ Add new tasks with title, description, due date, and priority
- 📋 List all tasks with sorting options
- ✏️ Update task details
- ✓ Mark tasks as completed
- 🗑️ Delete tasks
- 🔍 Filter tasks by priority, status, or due date
- 💾 Persistent storage using MongoDB

## Requirements

- Python 3.8 or higher
- MongoDB 4.0 or higher (running locally or remotely)

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd task_manager
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MongoDB

**On Windows:**
- Download MongoDB Community Server from https://www.mongodb.com/try/download/community
- Follow the installation wizard
- Start MongoDB service

### 4. Verify MongoDB is running

```bash
# Check if MongoDB is running
mongosh  # or mongo (for older versions)
```

You should see a MongoDB shell prompt. Type `exit` to quit.

## Project Structure

```
task_manager/
│
├── task.py              # Task class definition
├── database.py          # Database handler for MongoDB operations
├── task_manager.py      # TaskManager class with business logic
├── main.py              # CLI application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage

### Running the Application

```bash
python main.py
```

### Main Menu Options

```
1. Add a new task       - Create a new task with all details
2. List all tasks       - View all tasks with optional sorting
3. Update a task        - Modify existing task details
4. Mark task as completed - Change task status to completed
5. Delete a task        - Remove a task permanently
6. Filter tasks         - View tasks filtered by criteria
7. Exit                 - Close the application
```

### Example Workflow

1. **Add a task:**
   - Choose option 1
   - Enter task title (e.g., "Complete project report")
   - Enter description (e.g., "Finish the Q4 report")
   - Enter due date (e.g., "2026-03-15")
   - Select priority (Low, Medium, or High)

2. **List tasks:**
   - Choose option 2
   - Optionally sort by due date, priority, or creation date

3. **Update a task:**
   - Choose option 3
   - Enter the task ID (shown in the list)
   - Select what to update
   - Enter new value

4. **Mark as completed:**
   - Choose option 4
   - Enter the task ID

5. **Filter tasks:**
   - Choose option 6
   - Select filter criteria (priority, status, or due date)
   - Enter filter value

## Database Configuration

### Default Configuration

The application uses the following default MongoDB settings:
- **Connection String:** `mongodb://localhost:27017/`
- **Database Name:** `task_management`
- **Collection Name:** `tasks`

### Custom Configuration

To use a different MongoDB instance, modify the connection string in `database.py`:

```python
# In database.py, __init__ method
def __init__(self, connection_string: str = 'mongodb://your-custom-host:port/',
             database_name: str = 'your_database_name'):
```

Or modify the instantiation in `main.py`:

```python
# In main.py, TaskManagementCLI.__init__
self.db_handler = DatabaseHandler(
    connection_string='mongodb://your-host:port/',
    database_name='your_database'
)
```

### Database Schema

```javascript
{
  task_id: String,      // Unique identifier (8-character UUID)
  title: String,        // Task title
  description: String,  // Detailed description
  due_date: String,     // Due date (YYYY-MM-DD format)
  priority: String,     // Priority level (Low/Medium/High)
  status: String,       // Current status (Pending/In Progress/Completed)
  created_at: String    // Creation timestamp
}
```

## Testing

### Manual Testing Steps

1. **Test adding tasks:**
   ```
   - Add task with valid data ✓
   - Try adding task with invalid date format ✓
   - Try adding task with invalid priority ✓
   ```

2. **Test listing and sorting:**
   ```
   - List all tasks ✓
   - Sort by due date ✓
   - Sort by priority ✓
   ```

3. **Test updating:**
   ```
   - Update task title ✓
   - Update task status ✓
   - Try updating non-existent task ✓
   ```

4. **Test filtering:**
   ```
   - Filter by priority ✓
   - Filter by status ✓
   - Filter by due date ✓
   ```

5. **Test deletion:**
   ```
   - Delete existing task ✓
   - Try deleting non-existent task ✓
   ```

6. **Test persistence:**
   ```
   - Add tasks and exit ✓
   - Restart application ✓
   - Verify tasks are loaded ✓
   ```