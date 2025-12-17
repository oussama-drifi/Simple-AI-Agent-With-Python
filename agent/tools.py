from database.db import Database

def get_tasks(status=None, priority=None, deadline=None):
    conn = Database.get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE deleted_at IS NULL"
    params = []
    
    if status:
        query += " AND status = %s"
        params.append(status)
    if priority:
        query += " AND priority = %s"
        params.append(priority)
    if deadline:
        query += " AND DATE(deadline) = %s"
        params.append(deadline)
        
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def create_task(title, description=None, priority='medium', deadline=None):
    conn = Database.get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (title, description, priority, deadline, status) VALUES (%s, %s, %s, %s, 'todo')"
    cursor.execute(query, (title, description, priority, deadline))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "task_id": new_id, "message": f"Task '{title}' created."}

def update_task(task_id, status=None, priority=None, deadline=None):
    conn = Database.get_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if status: updates.append("status = %s"); params.append(status)
    if priority: updates.append("priority = %s"); params.append(priority)
    if deadline: updates.append("deadline = %s"); params.append(deadline)
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE task_id = %s"
    params.append(task_id)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Task {task_id} updated."}

def get_task_details(task_id):
    conn = Database.get_connection()
    cursor = conn.cursor(dictionary=True)
    # Get task and join sub-tasks
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.execute("SELECT * FROM sub_tasks WHERE task_id = %s AND deleted_at IS NULL", (task_id,))
    sub_tasks = cursor.fetchall()
    conn.close()
    return {"task": task, "sub_tasks": sub_tasks}

# Map for the loop
tools_dict = {
    "get_tasks": get_tasks,
    "create_task": create_task,
    "update_task": update_task,
    "get_task_details": get_task_details
}