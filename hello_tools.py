"""
Hello Tool Use - your first agent loop.

Claude is given two tools (weather + calculator). It must figure out which to call,
in what order, then synthesize a final answer. This is the foundation pattern under
every agent you'll build for the next 3 weeks.

Run:
    uv run python hello_tools.py
"""

import json

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables
client = Anthropic()  # automatically picks up ANTHROPIC_API_KEY

MODEL = "claude-sonnet-4-5"  # fast and cheap; perfect for tool-use demos

# ---------- Tool definitions (the "API" Claude sees) ----------
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current temperature in Celsius for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Tokyo' or 'Melbourne'",
                }
            },
            "required": ["city"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate a simple arithmetic expression. Supports + - * / and parentheses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Expression to evaluate, e.g. '23 * 17 + 4'",
                }
            },
            "required": ["expression"],
        },
    },
]


# ---------- Tool implementations (the actual code that runs) ----------
def get_weather(city: str) -> str:
    """Fake weather. In real apps this hits an API."""
    fake_temps = {"tokyo": 22, "melbourne": 18, "london": 12, "new york": 15}
    temp = fake_temps.get(city.lower(), 20)
    return json.dumps({"city": city, "temp_celsius": temp})


def calculator(expression: str) -> str:
    """Safe-ish eval - only digits and basic operators."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "Invalid characters in expression"})
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


TOOL_FNS = {
    "get_weather": lambda inp: get_weather(inp["city"]),
    "calculator": lambda inp: calculator(inp["expression"]),
}


# ---------- The agent loop ----------
def run(user_question: str, max_turns: int = 10) -> str:
    messages = [{"role": "user", "content": user_question}]

    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")

        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        print(f"stop_reason: {response.stop_reason}")
        print(f"tokens: in={response.usage.input_tokens} out={response.usage.output_tokens}")

        # Claude is done when stop_reason is 'end_turn' (no more tool calls)
        if response.stop_reason == "end_turn":
            final = next(
                (b.text for b in response.content if b.type == "text"),
                "(no text)",
            )
            return final

        # Otherwise stop_reason is 'tool_use' - execute every tool call, then loop
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  Tool call: {block.name}({block.input})")
                result = TOOL_FNS[block.name](block.input)
                print(f"  Result:    {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "user", "content": tool_results})

    return "(hit max turns without finishing)"


if __name__ == "__main__":
    question = (
        "What's the average temperature across Tokyo, London, and Melbourne?"
        "Show your reasoning."
    )
    print(f"Q: {question}\n")
    answer = run(question)
    print(f"\n=== FINAL ANSWER ===\n{answer}")