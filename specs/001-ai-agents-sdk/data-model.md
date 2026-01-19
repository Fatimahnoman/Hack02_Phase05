# Data Model: Conversational AI Layer

## Entities

### Conversation Context (Virtual Entity)
- **Purpose**: Represents the reconstructed conversation history provided to the AI agent
- **Components**:
  - All messages from the conversation ordered by timestamp
  - Formatted as a structured conversation history
  - Includes both user and assistant messages
- **Usage**: Used by the context builder to format conversation history for the agent

### Agent Configuration
- **Purpose**: Configuration parameters for the AI agent
- **Fields**:
  - model: String (AI model to use, e.g., "gpt-4", "gpt-3.5-turbo")
  - temperature: Float (creativity parameter, 0.0-2.0)
  - max_tokens: Integer (maximum tokens in response)
  - system_prompt: String (instructions for the agent's behavior)
- **Usage**: Used to configure the AI agent's behavior

### Message Formatting Specifications
- **Purpose**: Defines how messages are formatted for the AI agent
- **Structure**:
  - Role indicator (User/Assistant)
  - Message content
  - Timestamp (optional, for context)
- **Usage**: Used by the context builder to format messages for agent consumption

## State Transitions

### Agent Response Lifecycle
1. **Context Building**: Conversation history is fetched from database and formatted
2. **Agent Processing**: Formatted context is sent to the AI agent
3. **Response Generation**: Agent generates a response based on context
4. **Response Processing**: Response is validated and prepared for storage
5. **Persistence**: Agent response is saved to the database as an Assistant message
6. **Return**: Response is returned to the user

## Relationships

### Conversation ↔ Context Builder
- The Context Builder reads from the Conversation and Message entities
- Creates a formatted context for the AI agent
- Maintains the chronological order of messages

### AI Agent Service ↔ Message
- The AI Agent Service creates new Message entities for agent responses
- Stores the agent's response in the database
- Links the response to the appropriate conversation

## Constraints

### Context Window Management
- Total token count must not exceed the model's maximum context window
- Recent messages are prioritized over older ones when truncation is needed
- System must validate token count before sending to API

### Data Integrity
- Agent responses must be properly attributed to the correct conversation
- Message ordering must be preserved in the conversation history
- All messages must have proper role classification (user/assistant)

### Error Handling
- Failed agent responses must not corrupt the conversation history
- Fallback responses must be stored appropriately
- Error states must be logged for debugging