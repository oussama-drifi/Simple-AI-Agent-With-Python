import requests
import os

BASE_URL = os.getenv("CRUD_SERVICE_BASE_URL", "http://localhost:3000")


def get_tasks(status=None, priority=None, category=None, deadline=None):
    params = {k: v for k, v in {"status": status, "priority": priority, "category": category, "deadline": deadline}.items() if v}
    res = requests.get(f"{BASE_URL}/api/tasks", params=params)
    return res.json()


def get_task_details(task_id):
    res = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    return res.json()


def create_task(title, description=None, priority="medium", status="todo", category="other", deadline=None):
    body = {k: v for k, v in {"title": title, "description": description, "priority": priority, "status": status, "category": category, "deadline": deadline}.items() if v is not None}
    res = requests.post(f"{BASE_URL}/api/tasks", json=body)
    return res.json()


def update_task(task_id, title=None, description=None, priority=None, status=None, category=None, deadline=None):
    body = {k: v for k, v in {"title": title, "description": description, "priority": priority, "status": status, "category": category, "deadline": deadline}.items() if v is not None}
    res = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=body)
    return res.json()


def delete_task(task_id):
    res = requests.delete(f"{BASE_URL}/api/tasks/{task_id}")
    return res.json()


def create_subtask(task_id, title, description=None, deadline=None):
    body = {k: v for k, v in {"title": title, "description": description, "deadline": deadline}.items() if v is not None}
    res = requests.post(f"{BASE_URL}/api/tasks/{task_id}/subtasks", json=body)
    return res.json()


def update_subtask(task_id, sub_task_id, title=None, description=None, deadline=None, is_done=None):
    body = {k: v for k, v in {"title": title, "description": description, "deadline": deadline, "is_done": is_done}.items() if v is not None}
    res = requests.put(f"{BASE_URL}/api/tasks/{task_id}/subtasks/{sub_task_id}", json=body)
    return res.json()


def delete_subtask(task_id, sub_task_id):
    res = requests.delete(f"{BASE_URL}/api/tasks/{task_id}/subtasks/{sub_task_id}")
    return res.json()
