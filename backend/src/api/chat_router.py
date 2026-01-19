"""
API Router for chat endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator
from ..database import get_session
from ..models.message import MessageRead
from ..services.chat_service import ChatService
from ..config import settings
from uuid import UUID as UUIDType
import uuid


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > settings.max_message_length:
            raise ValueError(f'Message too long, maximum {settings.max_message_length} characters')
        return v

    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
            except ValueError:
                raise ValueError('Invalid conversation_id format')
        return v


class ChatResponse(BaseModel):
    conversation_id: str
    message: str


router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint to handle user messages and return assistant responses.
    Creates a new conversation if no conversation_id is provided,
    or continues an existing conversation if conversation_id is provided.
    """
    try:
        # Convert conversation_id from string to UUID if provided
        conversation_id_uuid = None
        if request.conversation_id:
            try:
                conversation_id_uuid = uuid.UUID(request.conversation_id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid conversation_id format")

        # Process the user message using the ChatService
        conversation, user_message, assistant_message = ChatService.process_user_message(
            session=session,
            user_id=user_id,
            user_message_content=request.message,
            conversation_id=conversation_id_uuid
        )

        # Return the response with conversation ID and assistant message
        return ChatResponse(
            conversation_id=str(conversation.id),
            message=assistant_message.content
        )

    except ValueError as e:
        # Handle case where conversation is not found
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")