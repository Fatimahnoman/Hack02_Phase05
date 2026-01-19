"""
AI Configuration model for the stateless chat API.
"""
from sqlmodel import SQLModel
from typing import Optional


class AIConfigBase(SQLModel):
    """
    Base model for AI configuration settings.
    """
    model: str
    temperature: float
    max_tokens: int
    system_prompt: Optional[str] = None


class AIConfig(AIConfigBase):
    """
    Model for AI agent configuration with default values.
    """
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: Optional[str] = "You are a helpful AI assistant. Use the conversation history to provide context-aware responses."


class AIConfigUpdate(SQLModel):
    """
    Model for updating AI configuration settings.
    """
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None