"""
LLM USE CASE: Tool / Function Calling
Examples: book flights, query CRM, call APIs, execute code

WHY function calling: structured JSON output → reliable tool invocation (vs parsing free text).
OpenAI / Anthropic / local models (Llama 3) all support this pattern.
"""

import json
from dataclasses import dataclass
from typing import Any


# --- 1. Define tool schemas (OpenAI format) ---
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search product catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
]


# --- 2. Implement actual tool functions ---
def get_weather(city: str, unit: str = "celsius") -> dict:
    return {"city": city, "temperature": 22, "unit": unit, "condition": "sunny"}


def search_products(query: str, max_results: int = 5) -> list:
    return [{"id": 1, "name": f"Product matching {query}"}]


TOOL_REGISTRY = {
    "get_weather": get_weather,
    "search_products": search_products,
}


# --- 3. OpenAI function calling loop ---
def run_with_tools(user_message: str, client, model: str = "gpt-4o-mini", max_rounds: int = 5):
    """
    WHY loop: model may call multiple tools before giving final answer.
    Flow: user msg → model requests tool → execute → feed result back → repeat.
    """
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_rounds):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content  # final answer

        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            result = TOOL_REGISTRY[fn_name](**fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    return "Max rounds reached"


# --- 4. Local model tool calling (Llama 3 JSON mode) ---
def parse_tool_call_from_text(text: str) -> dict | None:
    """
    WHY fallback parser: open-source models may output JSON in text instead of native tool_calls.
    """
    try:
        start = text.index("{")
        return json.loads(text[start:])
    except (ValueError, json.JSONDecodeError):
        return None
