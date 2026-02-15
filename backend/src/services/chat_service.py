"""
Service layer for chat-related operations.
"""
import logging
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole
from .conversation_service import ConversationService
from .ai_agent_service import AIAgentService
from .context_builder import ContextBuilder
from .ai_error_handler import ai_fallback_handler, AIServiceError
from ..nlp.intent_parser import IntentParser
from ..nlp.utils import parse_natural_language_command
from ..models.task import TaskCreate
from .task_service import TaskService

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service class for handling chat operations.
    """

    @staticmethod
    def process_user_message(
        session: Session,
        user_id: str,
        user_message_content: str,
        conversation_id: Optional[UUID] = None
    ) -> tuple[Conversation, Message, Message]:
        """
        Process a user message and return the conversation, user message, and assistant response.

        Args:
            session: Database session
            user_id: ID of the user sending the message
            user_message_content: Content of the user's message
            conversation_id: Optional conversation ID to continue existing conversation

        Returns:
            Tuple of (conversation, user_message, assistant_response)
        """
        logger.info(f"Processing user message for user_id: {user_id}, conversation_id: {conversation_id}")

        # Get or create conversation
        if conversation_id:
            conversation = ConversationService.get_conversation_by_id(session, conversation_id)
            if not conversation:
                logger.warning(f"Conversation with ID {conversation_id} not found for user {user_id}")
                raise ValueError(f"Conversation with ID {conversation_id} not found")
        else:
            logger.info(f"Creating new conversation for user {user_id}")
            conversation = ConversationService.create_conversation(session, user_id)
            logger.info(f"Created new conversation with ID {conversation.id}")

        # Create and save user message
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content=user_message_content
        )
        session.add(user_message)
        session.commit()
        session.refresh(user_message)
        logger.info(f"Saved user message with ID {user_message.id} to conversation {conversation.id}")

        # Generate assistant response based on conversation history
        logger.info(f"Generating assistant response for conversation {conversation.id}")
        assistant_response = ChatService._generate_assistant_response(session, conversation.id)

        # Update conversation timestamp
        ConversationService.update_conversation_timestamp(session, conversation)
        logger.info(f"Updated conversation {conversation.id} timestamp after processing message")

        return conversation, user_message, assistant_response

    @staticmethod
    def _generate_assistant_response(session: Session, conversation_id: UUID) -> Message:
        """
        Generate an AI-powered assistant response based on conversation history.
        This method now integrates with the AI agent service for context-aware responses.
        """
        logger.info(f"Getting conversation history for AI response generation, conversation_id: {conversation_id}")

        # Get conversation history to inform the response
        conversation_history = ChatService._get_conversation_history(session, conversation_id)
        logger.info(f"Retrieved {len(conversation_history)} messages from conversation history")

        # Generate AI response using the AI agent service
        logger.info("Generating AI-powered assistant response")

        # Use the AI agent service with fallback handling
        response_text = ChatService._generate_ai_response_with_fallback(
            session, conversation_id, conversation_history
        )

        # Validate the response before saving
        if not AIAgentService.validate_response(response_text):
            logger.warning("AI response failed validation, using fallback")
            from ..config import settings
            response_text = settings.fallback_response

        # Create and save assistant message
        logger.info(f"Creating assistant message with content: {response_text[:50]}...")
        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.assistant,
            content=response_text
        )
        session.add(assistant_message)
        session.commit()
        session.refresh(assistant_message)
        logger.info(f"Saved assistant message with ID {assistant_message.id}")

        # Invalidate the context cache for this conversation since it has changed
        from .context_builder import ContextBuilder
        ContextBuilder.invalidate_cache(conversation_id)

        return assistant_message

    @staticmethod
    @ai_fallback_handler()
    def _generate_ai_response_with_fallback(session: Session, conversation_id: UUID, conversation_history: List[Message]) -> str:
        """
        Generate AI response with fallback handling in case of AI service failures.
        """
        from ..config import settings

        # Check if the last message contains a command for creating/updating tasks
        if conversation_history:
            last_message = conversation_history[-1]
            user_input = last_message.content.lower()
            
            # Check if this looks like a task creation/update command
            task_keywords = ['create task', 'add task', 'make task', 'set priority', 'add tag', 'due date', 'remind me', 'every', 'recurring']
            if any(keyword in user_input for keyword in task_keywords):
                # Parse the natural language command
                try:
                    task_create_obj = parse_natural_language_command(last_message.content)
                    
                    # Create the task using the task service
                    task_service = TaskService()
                    created_task = task_service.create_task(session, task_create_obj)
                    
                    # Return a confirmation message
                    return f"I've created the task '{created_task.title}' with priority {created_task.priority}."
                except Exception as e:
                    logger.error(f"Error processing task command: {str(e)}")
                    # If task processing fails, fall back to normal AI response
        
        # Build context for the AI agent
        context_messages = ContextBuilder.build_context_from_conversation(
            session,
            conversation_id,
            max_tokens=settings.max_context_tokens
        )

        # Generate response using AI agent
        ai_response = AIAgentService.generate_response(
            conversation_history=context_messages,
            system_prompt="You are a helpful AI assistant. Use the conversation history to provide context-aware responses."
        )

        # Validate the response
        if not AIAgentService.validate_response(ai_response):
            logger.warning("AI response failed validation, using fallback")
            raise AIServiceError("AI response validation failed")

        return ai_response

    @staticmethod
    def _get_conversation_history(session: Session, conversation_id: UUID) -> List[Message]:
        """
        Retrieve the conversation history for a given conversation ID.
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp)
        messages = session.exec(statement).all()
        return messages

    @staticmethod
    def _create_placeholder_response(conversation_history: List[Message]) -> str:
        """
        Create a placeholder response based on the conversation history.
        This is a minimal implementation that just returns a generic response.
        """
        logger.info(f"Creating placeholder response based on {len(conversation_history)} messages in history")

        # In a real implementation, this would analyze the conversation history
        # and generate an appropriate response using an LLM
        # For now, we'll return a simple but more contextual response
        if len(conversation_history) <= 2:  # First few messages
            return "Hello! I'm your AI assistant. I've received your message and I'm ready to help. What would you like to know?"
        else:
            return "Thank you for your message. I'm processing your request and will assist you shortly. How else can I help you?"