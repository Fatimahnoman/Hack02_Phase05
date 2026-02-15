import asyncio
from typing import Dict, Any, Callable
from dapr.aio.clients import DaprClient
from pydantic import BaseModel
import json


class EventPayload(BaseModel):
    """Base class for event payloads."""
    event_type: str
    data: Dict[str, Any]
    timestamp: float


class DaprPubSubUtils:
    """Utilities for Dapr pub/sub operations."""
    
    def __init__(self, dapr_client: DaprClient = None):
        self._client = dapr_client
    
    async def get_client(self) -> DaprClient:
        """Get or create a Dapr client instance."""
        if self._client is None:
            self._client = DaprClient()
        return self._client
    
    async def publish_event(self, pubsub_name: str, topic_name: str, payload: EventPayload) -> None:
        """Publish an event to Dapr pub/sub."""
        client = await self.get_client()
        await client.publish_event(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=json.dumps(payload.dict()),
            data_content_type='application/json'
        )
    
    async def subscribe_to_topic(self, pubsub_name: str, topic_name: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to a topic and handle incoming events."""
        # Note: Actual subscription in Dapr typically happens at the application level
        # This is a utility method to encapsulate subscription logic
        pass
    
    async def close(self) -> None:
        """Close the Dapr client connection."""
        if self._client:
            await self._client.close()