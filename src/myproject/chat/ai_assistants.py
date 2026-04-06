"""Django AI Assistant configuration.

This file defines AI assistants using the django-ai-assistant package.
The package auto-discovers this file (ai_assistants.py convention).

To use with vLLM instead of OpenAI, set these environment variables:
    AI_ASSISTANT_OPENAI_API_BASE=http://your-vllm-server:8000/v1
    AI_ASSISTANT_OPENAI_API_KEY=EMPTY  (or your vLLM API key)
    AI_ASSISTANT_MODEL=your-model-name

See docs/ai-assistant-setup.md for detailed configuration instructions.
"""
import os

from django_ai_assistant import AIAssistant


class ProjectAssistant(AIAssistant):
    """Main project AI assistant."""

    id = "project-assistant"  # noqa: A003
    name = "Project Assistant"
    instructions = (
        "You are a helpful assistant for My Project. "  # TODO: Customize instructions
        "Answer questions clearly and concisely."
    )
    model = os.environ.get("AI_ASSISTANT_MODEL", "gpt-4o")  # TODO: Set your model

    def get_llm(self):
        """Override to support vLLM or custom OpenAI-compatible endpoints.

        If AI_ASSISTANT_OPENAI_API_BASE is set, uses that as the base URL.
        This enables vLLM, Azure OpenAI, or any OpenAI-compatible API.
        """
        from langchain_openai import ChatOpenAI

        api_base = os.environ.get("AI_ASSISTANT_OPENAI_API_BASE", "https://api.openai.com/v1")
        api_key = os.environ.get("AI_ASSISTANT_OPENAI_API_KEY", "")  # TODO: Set your API key

        return ChatOpenAI(
            model=self.model,
            openai_api_base=api_base,
            openai_api_key=api_key,
            temperature=0.7,  # TODO: Adjust as needed
        )
