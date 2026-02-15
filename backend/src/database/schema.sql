-- Database schema for Todo Chatbot with Phase V features

-- Indexes for Task table performance
CREATE INDEX idx_task_user_id ON task (user_id);
CREATE INDEX idx_task_priority ON task (user_id, priority);
CREATE INDEX idx_task_due_date ON task (user_id, due_date);
CREATE INDEX idx_task_status ON task (user_id, status);
CREATE INDEX idx_task_created_at ON task (user_id, created_at);

-- Full-text search indexes for task title and description
CREATE INDEX idx_task_title_gin ON task USING gin(to_tsvector('english', title));
CREATE INDEX idx_task_description_gin ON task USING gin(to_tsvector('english', description));
CREATE INDEX idx_task_full_text ON task USING gin((to_tsvector('english', title || ' ' || COALESCE(description, ''))));

-- Indexes for Tag table
CREATE INDEX idx_tag_user_id_name ON tag (user_id, name);

-- Indexes for RecurringTaskPattern table
CREATE INDEX idx_recurring_pattern_user_id ON recurringtaskpattern (user_id);
CREATE INDEX idx_recurring_pattern_start_date ON recurringtaskpattern (user_id, start_date);
CREATE INDEX idx_recurring_pattern_recurrence_type ON recurringtaskpattern (user_id, recurrence_type);

-- Indexes for Reminder table
CREATE INDEX idx_reminder_task_id ON reminder (task_id);
CREATE INDEX idx_reminder_reminder_datetime ON reminder (reminder_datetime, sent, dismissed);
CREATE INDEX idx_reminder_user_id ON reminder (task_id); -- Indirect user access via task

-- Foreign key constraints
ALTER TABLE task ADD CONSTRAINT fk_task_recurring_pattern FOREIGN KEY (recurring_pattern_id) REFERENCES recurringtaskpattern(id);

-- Many-to-many relationship indexes
CREATE INDEX idx_task_tag_task_id ON task_tag (task_id);
CREATE INDEX idx_task_tag_tag_id ON task_tag (tag_id);