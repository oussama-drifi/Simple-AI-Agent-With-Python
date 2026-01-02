from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

# these are parent classes (DRY principle)

class TaskBase(BaseModel):
    """Base model for task-related schemas"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the task", examples=["Buy groceries", "Finish report", "Call doctor"])
    description: Optional[str] = Field(None, description="Detailed description of the task", examples=["Get milk, eggs, and bread", "Complete Q4 financial analysis"])
    deadline: Optional[datetime] = Field(None, description="When the task is due (ISO format: YYYY-MM-DDTHH:MM:SS)", examples=["2024-12-31T23:59:59", "2024-06-15T12:00:00"])
    category: Optional[str] = Field("other", max_length=100, description="Task category", examples=["work", "personal", "shopping", "health", "finance"])

# request models
class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    priority: Literal["low", "medium", "high"] = Field("medium", description="Priority level of the task")
    status: Literal["todo", "in progress", "canceled", "done"] = Field("todo", description="Current status of the task")
    
class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    deadline: Optional[datetime] = Field(None, description="New deadline for the task")
    category: Optional[str] = Field(None, max_length=100, description="New category for the task")
    priority: Optional[Literal["low", "medium", "high"]] = Field(None, description="New priority level")
    status: Optional[Literal["todo", "in progress", "canceled", "completed"]] = Field(None, description="New status")

# models to retrieve from database
class TaskResponse(TaskBase):
    """Model for task responses (includes all DB fields)"""
    # what the database returns
    task_id: int = Field(..., description="Unique task identifier")
    priority: str = Field(..., description="Priority level")
    status: str = Field(..., description="Current status")
    creation_date: datetime = Field(..., description="When the task was created")
    updated_date: Optional[datetime] = Field(None, description="Last update time")
    deleted_at: Optional[datetime] = Field(None, description="When task was deleted")
    model_config = ConfigDict(from_attributes=True)