"""
LLM USE CASE: AI Agent (ReAct pattern)
Examples: research assistant, data analyst agent, multi-step task solver

WHY agent vs single prompt: complex tasks need planning, tool use, and self-correction.
WHY ReAct (Reason + Act): interleaves thinking and tool calls → more reliable than blind tool use.
"""

from dataclasses import dataclass
from typing import Callable

# pip install langchain langchain-openai


@dataclass
class Tool:
    name: str
    description: str
    func: Callable


# --- Define tools the agent can call ---
def search_web(query: str) -> str:
    """WHY search tool: LLM knowledge has cutoff date; needs live data."""
    return f"[search results for: {query}]"


def calculator(expression: str) -> str:
    """WHY calculator: LLMs are bad at exact math."""
    try:
        return str(eval(expression))  # use safe math parser in production
    except Exception as e:
        return f"Error: {e}"


def query_database(sql: str) -> str:
    """WHY DB tool: agent accesses structured company data."""
    return f"[DB result for: {sql}]"


TOOLS = [
    Tool("search", "Search the web for current information. Input: search query.", search_web),
    Tool("calculator", "Evaluate a math expression. Input: math expression string.", calculator),
    Tool("database", "Run SQL query on company database. Input: SQL string.", query_database),
]


REACT_PROMPT = """You are an agent that solves tasks using tools.

Available tools:
{tool_descriptions}

Use this format:
Thought: <your reasoning>
Action: <tool_name>
Action Input: <input to tool>
Observation: <tool result — filled by system>
... (repeat Thought/Action/Observation as needed)
Thought: I have enough information
Final Answer: <your answer>

Question: {question}
{scratchpad}"""


def build_tool_descriptions(tools: list[Tool]) -> str:
    return "\n".join(f"- {t.name}: {t.description}" for t in tools)


def get_tool(name: str) -> Tool:
    return next(t for t in TOOLS if t.name == name)


def run_react_agent(question: str, llm, max_steps: int = 5) -> str:
    """
    WHY manual loop vs LangChain AgentExecutor: shows you understand the pattern.
    In interview: explain loop, then mention LangChain/LlamaIndex as production wrappers.
    """
    scratchpad = ""
    tool_desc = build_tool_descriptions(TOOLS)

    for _ in range(max_steps):
        prompt = REACT_PROMPT.format(
            tool_descriptions=tool_desc, question=question, scratchpad=scratchpad
        )
        response = llm.generate(prompt)

        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        if "Action:" in response and "Action Input:" in response:
            action = response.split("Action:")[1].split("\n")[0].strip()
            action_input = response.split("Action Input:")[1].split("\n")[0].strip()
            tool = get_tool(action)
            observation = tool.func(action_input)
            scratchpad += response + f"\nObservation: {observation}\n"

    return "Max steps reached without answer"


# --- LangChain agent (production shortcut) ---
def build_langchain_agent():
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_openai import ChatOpenAI
    from langchain.tools import Tool as LCTool

    tools = [
        LCTool(name="search", func=search_web, description="Search the web"),
        LCTool(name="calculator", func=calculator, description="Math calculator"),
    ]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools, REACT_PROMPT)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
