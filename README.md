# TaskCat

## Database Migrations

### Running Migrations

To run a specific migration:

```bash
# Navigate to the project root
cd /path/to/taskcat

# Run a specific migration
python -m src.scripts.run_migration <migration_file_name>

# Example:
python -m src.scripts.run_migration add_difficulty_points_to_tasks.sql
```

This will execute the SQL statements in the specified migration file against the database.

## Task Data Structure

After running the `add_difficulty_points_to_tasks.sql` migration, the tasks list now includes the following additional fields:

- `difficulty`: Indicates the difficulty level of the task (integer, 1-5 scale)
- `points`: The number of points awarded for completing the task (integer)

These fields are now automatically included in all task list responses. When you call the GET `/api/v1/tasks/` endpoint, these fields will be included in each task object in the response.

### Example Response

```json
[
  {
    "id": 1,
    "title": "Implement login page",
    "description": "Create a new login page with username and password fields",
    "status": "pending",
    "progress": 0,
    "difficulty": 2,
    "points": 50,
    "creator_id": 1,
    "assignee_id": null,
    "created_at": "2023-07-01T10:30:00",
    "updated_at": null
  },
  // More tasks...
]
```
