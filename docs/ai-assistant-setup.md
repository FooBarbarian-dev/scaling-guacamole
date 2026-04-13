# AI Assistant Setup

This project uses [Django AI Assistant](https://github.com/vintasoftware/django-ai-assistant) to provide chat functionality. The assistant configuration lives in `src/myproject/chat/ai_assistants.py`.

## Configuration

### Environment Variables

Set these in your `.env` file:

```bash
# For OpenAI (default)
AI_ASSISTANT_OPENAI_API_BASE=https://api.openai.com/v1
AI_ASSISTANT_OPENAI_API_KEY=sk-your-key-here  # TODO: Set your OpenAI API key
AI_ASSISTANT_MODEL=gpt-4o                      # TODO: Set your model name

# For vLLM
AI_ASSISTANT_OPENAI_API_BASE=http://your-vllm-server:8000/v1  # TODO: Set your vLLM URL
AI_ASSISTANT_OPENAI_API_KEY=EMPTY                               # Or your vLLM API key
AI_ASSISTANT_MODEL=your-model-name                              # TODO: Set your model name
```

### How It Works

Django AI Assistant uses LangChain internally. The `ai_assistants.py` file defines assistant classes that inherit from `AIAssistant`:

```python
from django_ai_assistant import AIAssistant

class ProjectAssistant(AIAssistant):
    id = "project-assistant"
    name = "Project Assistant"
    instructions = "You are a helpful assistant."
    model = "gpt-4o"

    def get_llm(self):
        # Override to use custom endpoint (vLLM, Azure, etc.)
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=self.model,
            openai_api_base="http://your-vllm:8000/v1",
            openai_api_key="EMPTY",
        )
```

### Using vLLM

To use a vLLM instance instead of OpenAI:

1. Set `AI_ASSISTANT_OPENAI_API_BASE` to your vLLM server URL with `/v1` suffix
2. Set `AI_ASSISTANT_OPENAI_API_KEY` to `EMPTY` (or your vLLM API key if configured)
3. Set `AI_ASSISTANT_MODEL` to the model name loaded in your vLLM instance

The `get_llm()` override in `ai_assistants.py` handles pointing LangChain's `ChatOpenAI` to your custom endpoint. vLLM exposes an OpenAI-compatible API, so no other changes are needed.

<!-- TODO: Add vLLM instance URL -->
<!-- TODO: Add model name -->
<!-- TODO: Add any model-specific parameters (temperature, max_tokens, etc.) -->

### Adding New Assistants

1. Open `src/myproject/chat/ai_assistants.py`
2. Create a new class inheriting from `AIAssistant`
3. Set a unique `id`, `name`, `instructions`, and `model`
4. Optionally override `get_llm()` for custom LLM providers
5. The assistant is auto-discovered by Django AI Assistant

### URL Configuration

The AI assistant URLs are included at `/ai-assistant/` in the root URL config:

```python
path("ai-assistant/", include("django_ai_assistant.urls"))
```

This provides the API endpoints that the chat interface uses to communicate with the assistant.
