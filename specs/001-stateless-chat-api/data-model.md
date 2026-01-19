# Data Model: Stateless Chat API

## Entities

### Conversation
- **Fields**:
  - id: UUID (primary key, unique identifier for conversation)
  - user_id: String (identifier for the user who owns this conversation)
  - created_at: DateTime (timestamp when conversation was created)
  - updated_at: DateTime (timestamp when conversation was last updated)
- **Relationships**:
  - Has many Messages (one-to-many relationship)
- **Validation rules**:
  - user_id must be provided
  - created_at and updated_at are automatically managed by the system
  - id is auto-generated as UUID

### Message
- **Fields**:
  - id: UUID (primary key, unique identifier for message)
  - conversation_id: UUID (foreign key linking to Conversation)
  - role: String (enum: 'user' or 'assistant', indicates sender type)
  - content: String (the actual message content)
  - timestamp: DateTime (when the message was created)
- **Relationships**:
  - Belongs to Conversation (many-to-one relationship)
- **Validation rules**:
  - conversation_id must reference an existing conversation
  - role must be either 'user' or 'assistant'
  - content must not be empty
  - timestamp is automatically set when message is created

## State Transitions

### Conversation Lifecycle
1. **Creation**: New conversation is created when no conversation_id is provided in request
2. **Active**: Conversation receives messages and grows in length
3. **Inactive**: Conversation exists in database but no recent activity
4. **Deletion**: Conversation may be deleted based on retention policy (future feature)

### Message Lifecycle
1. **Received**: User message is received by the system
2. **Stored**: User message is persisted in the database
3. **Processed**: Assistant generates response based on conversation history
4. **Responded**: Assistant message is generated and stored in database
5. **Retrieved**: Both user and assistant messages are retrieved for response

## Relationships

### Conversation ↔ Message
- One Conversation can have many Messages (one-to-many)
- Each Message belongs to exactly one Conversation
- Foreign key constraint ensures referential integrity
- Cascade deletion may be implemented to clean up messages when conversation is deleted

## Indexing Strategy

### Primary Indexes
- Conversation.id (UUID, primary key)
- Message.id (UUID, primary key)

### Secondary Indexes
- Conversation.user_id (for user-specific queries)
- Message.conversation_id (for conversation history retrieval)
- Message.timestamp (for chronological ordering)
- Message.role (for filtering by message type)

## Constraints

### Data Integrity
- Foreign key constraints to maintain referential integrity
- Non-null constraints on required fields
- Check constraints on role field (must be 'user' or 'assistant')
- Unique constraints where appropriate

### Business Logic
- Conversation.user_id must match the authenticated user context
- Messages can only be added to existing conversations
- Message content must be provided and non-empty