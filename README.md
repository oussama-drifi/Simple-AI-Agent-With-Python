# Simple AI Agent — Task Manager

A conversational AI agent service built with Flask and Gemini 2.5 Flash. It exposes a single chat endpoint that lets users manage their tasks through natural language. All data operations are delegated to an external CRUD service via HTTP.

## Architecture

```
Client (React / any)
      │
      ▼
 AI Agent Service  (this repo — Python/Flask, port 5000)
      │  POST /api/chat
      │  Gemini 2.5 Flash + tool calling
      │
      ▼
 Task CRUD Service  (separate service — port 3000)
      │
      ▼
   MySQL DB
```

The agent receives a user prompt and a conversation history, runs an agentic loop (up to 5 turns) calling tools as needed, and returns the final response along with the updated history. The client is responsible for persisting and replaying history on each request (stateless backend).

## Tech Stack

- **Flask** — HTTP server
- **Flask-CORS** — Cross-origin resource sharing
- **Google GenAI SDK** — Gemini 2.5 Flash with function calling
- **python-dotenv** — Environment config

## Getting Started

### Prerequisites

- Python 3.11+
- A running instance of the Task CRUD Service

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the root:

```env
# Flask
SECRET_KEY=your_secret_key
PORT=5000
DEBUG_MODE=0

# Gemini
GEMINI_API_KEY=your_gemini_api_key

# CORS — origin of your front-end
CORS_ORIGIN=http://localhost:5173

# External CRUD service
CRUD_SERVICE_BASE_URL=http://localhost:3000
```

### Run

```bash
python app.py
```

## API

### `POST /api/chat`

**Body:**
```json
{
  "user_prompt": "Create a high priority task called 'Deploy to production' due next Monday",
  "history": []
}
```

**Response:**
```json
{
  "response": "Done! I've created the task 'Deploy to production' with high priority...",
  "history": [...]
}
```

`history` is an array of Gemini `Content` objects. Pass the returned `history` back on the next request to maintain conversation context.

---

## External CRUD Service Endpoints

The agent calls the following endpoints on the Task CRUD Service:

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List tasks (filterable) |
| GET | `/api/tasks/:id` | Get a single task with its sub-tasks |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/:id` | Update a task |
| DELETE | `/api/tasks/:id` | Soft-delete a task |

**`GET /api/tasks` query params:** `status`, `priority`, `category`, `deadline` (YYYY-MM-DD)

**`POST /api/tasks` body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "status": "todo",
  "category": "personal",
  "deadline": "2026-05-20T18:00:00"
}
```

**`PUT /api/tasks/:id` body** (all fields optional):
```json
{
  "title": "Buy groceries",
  "description": "Updated list",
  "priority": "high",
  "status": "in progress",
  "category": "personal",
  "deadline": "2026-05-21T18:00:00"
}
```

### Sub-tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/:id/subtasks` | Add a sub-task to a task |
| PUT | `/api/tasks/:id/subtasks/:sub_task_id` | Update a sub-task (title, description, deadline, is_done) |
| DELETE | `/api/tasks/:id/subtasks/:sub_task_id` | Soft-delete a sub-task |

**`POST /api/tasks/:id/subtasks` body:**
```json
{
  "title": "Write unit tests",
  "description": "Cover edge cases",
  "deadline": "2026-05-22T18:00:00"
}
```

**`PUT /api/tasks/:id/subtasks/:sub_task_id` body** (all fields optional):
```json
{
  "title": "Write unit tests",
  "description": "Updated scope",
  "deadline": "2026-05-23T18:00:00",
  "is_done": true
}
```

---

## Database Schema

### `tasks`

| Column | Type | Notes |
|--------|------|-------|
| `task_id` | INT (PK, auto-increment) | |
| `title` | VARCHAR(255) | required |
| `description` | TEXT | nullable |
| `deadline` | DATETIME | nullable |
| `creation_date` | DATETIME | default: now |
| `category` | VARCHAR(100) | default: `other` |
| `priority` | ENUM(`low`, `medium`, `high`) | default: `medium` |
| `status` | ENUM(`todo`, `in progress`, `canceled`, `completed`) | default: `todo` |
| `updated_date` | DATETIME | auto-updated |
| `deleted_at` | DATETIME | nullable — soft delete |

### `sub_tasks`

| Column | Type | Notes |
|--------|------|-------|
| `sub_task_id` | INT (PK, auto-increment) | |
| `title` | VARCHAR(255) | required |
| `description` | TEXT | nullable |
| `deadline` | DATETIME | required |
| `creation_date` | DATETIME | default: now |
| `is_done` | TINYINT(1) | default: 0 |
| `task_id` | INT (FK → tasks) | CASCADE DELETE |
| `updated_date` | DATETIME | auto-updated |
| `deleted_at` | DATETIME | nullable — soft delete |
