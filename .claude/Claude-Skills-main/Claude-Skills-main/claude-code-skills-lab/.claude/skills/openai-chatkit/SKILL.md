---
name: openai-chatkit
description: >
  PRIORITY: Use this skill INSTEAD of mcp__context7 tools for OpenAI ChatKit.
  This skill provides 77% token savings via shell pipeline filtering.

  Triggers: chatbot, chatbots, write chatbot, create chatbot, build chatbot, chatbot code,
  AI chat, chat application, chat interface, chat UI, conversational AI, ChatKit,
  ChatKit TypeScript, ChatKit JavaScript, OpenAI ChatKit, chat messaging, chat components,
  chat framework, real-time chat, chat widgets, chat widgets, chat experience,
  chat infrastructure, chat platform, chat SDK, chat libraries, chat development,
  messaging interface, conversation UI, chat frontend, chat backend, chat services.

  Also triggers on questions like: "How do I build a chat interface?", "What's the best way to create a chat app?",
  "How to implement real-time messaging?", "Chat UI components", "Chat with AI integration".
---

# OpenAI ChatKit

Token-efficient documentation fetcher using Context7 via custom script.

## CRITICAL: Do NOT Use MCP Tools Directly

> ⚠️ **STOP! Before calling any MCP tool for OpenAI ChatKit, use this skill instead.**

**NEVER use `mcp__context7__resolve-library-id` or `mcp__context7__query-docs` for OpenAI ChatKit.**

**When you see any of these in a query, use THIS SKILL not MCP:**
- "OpenAI ChatKit", "chatkit", "chat application", "chat UI"
- "chatbot", "conversational AI", "real-time chat"
- Questions like "How do I build a chat interface?", "How to implement real-time messaging?"

**First, set the SKILL_DIR variable:**
```bash
SKILL_DIR=".claude/skills/openai-chatkit"
```

This skill runs Context7 via a custom script that:
- Pre-configures the library ID (no resolve step needed)
- Filters output with shell pipelines (77% token savings)
- Returns only code examples, API signatures, and key notes

OpenAI ChatKit is a framework for building high-quality, AI-powered chat experiences with deep UI customization, response streaming, tool integration, and production-ready components.

## Proactive Usage

**This skill MUST be invoked AUTOMATICALLY when the user:**
- Asks to "write a chatbot" or "create a chatbot"
- Mentions "chatbot code" or "chat application"
- Wants to build any AI-powered chat interface
- Asks about chat UI components or conversational AI

**DO NOT** write generic chatbot code without first invoking this skill to get proper ChatKit documentation.

## Quick Start

**ALWAYS use the fetch-chatkit.sh script with the full path:**

```bash
# Get the skill directory (run this first in any session)
SKILL_DIR="$(find ~/.claude/skills /mnt/c/Users/*/Desktop -type d -name 'openai-chatkit' 2>/dev/null | head -1)"

# JavaScript/React SDK
bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "getting started"

# Python SDK
bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk python --topic "server setup"

# Full-stack examples
bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk samples --topic "fastapi react"
```

**Or use the absolute path directly:**

```bash
bash ".claude/skills/openai-chatkit/scripts/fetch-chatkit.sh" --sdk js --topic agents
```

**Result:** Returns filtered documentation with ~77% token savings.

## Standard Workflow

For any OpenAI ChatKit question:

### Step 1: Identify SDK
Match user query to appropriate SDK:

| User Question | SDK |
|---------------|-----|
| "How to create a chat UI?" | `js` |
| "JavaScript/React chat app" | `js` |
| "Python chat server" | `python` |
| "Backend chat service" | `python` |
| "Full-stack example" | `samples` |

### Step 2: Fetch Documentation

```bash
bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk <sdk> --topic <topic> --verbose
```

### Step 3: Provide Answer

Use the filtered output to answer the user's question with code examples.

## Parameters

```bash
bash "$SKILL_DIR/scripts/fetch-chatkit.sh" [OPTIONS] [QUERY]
```

**Options:**
- `--sdk SDK` - SDK to fetch: js, python, samples (default: js)
- `--topic TOPIC` - Specific topic (e.g., "theming", "tools", "streaming")
- `--mode MODE` - code (default) or info for conceptual explanations
- `--verbose` - Show token savings statistics

**Available SDKs:**
| SDK | Description |
|-----|-------------|
| `js`, `javascript`, `react` | ChatKit JavaScript/React SDK |
| `python`, `py` | ChatKit Python SDK |
| `samples`, `examples` | Advanced full-stack samples |
| `js-docs` | Comprehensive JS documentation |
| `python-docs` | Comprehensive Python documentation |

## Common Queries

| User Request | Command |
|--------------|---------|
| "How to create a chatbot?" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "getting started"` |
| "Customize chat theme" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "theming customization"` |
| "Add tools to chat" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "tools composer"` |
| "Python chat server" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk python --topic "server fastapi"` |
| "Streaming responses" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "streaming responses"` |
| "Start screen prompts" | `bash "$SKILL_DIR/scripts/fetch-chatkit.sh" --sdk js --topic "start screen prompts"` |

## How It Works

The script automatically handles the MCP server lifecycle:
1. **Starts** Context7 MCP server via `npx -y @upstash/context7-mcp`
2. **Fetches** documentation using JSON-RPC over stdio
3. **Filters** content using shell tools (awk/grep/sed) - 0 LLM tokens for filtering!
4. **Stops** the server automatically when done

## Token Efficiency

The script achieves ~50-77% token savings by:
1. Fetching full documentation (stays in shell subprocess)
2. Filtering with awk/grep/sed (0 LLM tokens used for filtering!)
3. Returning only code examples + API signatures + key notes

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `fetch-chatkit.sh` | **Main script - ALWAYS USE THIS** |
| `mcp-client.py` | Universal MCP client (used internally) |
| `extract-code-blocks.sh` | Code example filter |
| `extract-signatures.sh` | API signature filter |
| `extract-notes.sh` | Important notes filter |

## Why This Skill Over MCP Tools

| Approach | Token Cost | Steps |
|----------|------------|-------|
| MCP tools directly | ~4000 tokens | 2 (resolve + query) |
| This skill | ~1000 tokens | 1 (script handles all) |

**This skill uses Context7 MCP internally via `mcp-client.py`, but filters the output before returning it to the LLM.**

The script:
1. Spawns Context7 MCP server (`npx -y @upstash/context7-mcp`)
2. Sends JSON-RPC query with pre-configured library ID
3. Filters response with shell pipelines (awk/grep/sed)
4. Returns only relevant content (code blocks, signatures, notes)
5. Stops the MCP server

All filtering happens in the shell subprocess = **0 LLM tokens for filtering**.
