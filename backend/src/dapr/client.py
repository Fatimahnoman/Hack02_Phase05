import asyncio
from typing import Dict, Any, Optional
from dapr.aio.clients import DaprClient


class DaprClientWrapper:
    """Wrapper class for Dapr client to handle state management and pub/sub operations."""
    
    def __init__(self, dapr_client: DaprClient = None):
        self._client = dapr_client
    
    async def get_client(self) -> DaprClient:
        """Get or create a Dapr client instance."""
        if self._client is None:
            self._client = DaprClient()
        return self._client
    
    async def save_state(self, store_name: str, key: str, value: Any) -> None:
        """Save state to Dapr state store."""
        client = await self.get_client()
        await client.save_state(store_name, key, value)
    
    async def get_state(self, store_name: str, key: str) -> Any:
        """Get state from Dapr state store."""
        client = await self.get_client()
        response = await client.get_state(store_name, key)
        return response.data
    
    async def delete_state(self, store_name: str, key: str) -> None:
        """Delete state from Dapr state store."""
        client = await self.get_client()
        await client.delete_state(store_name, key)
    
    async def publish_event(self, pubsub_name: str, topic_name: str, data: Any) -> None:
        """Publish an event to Dapr pub/sub."""
        client = await self.get_client()
        await client.publish_event(pubsub_name, topic_name, data)
    
    async def close(self) -> None:
        """Close the Dapr client connection."""
        if self._client:
            await self._client.close()