from agno.tools import tool
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from knowledge import load_settings
from agno.agent import Agent

@tool(
    description="Your Subagent for Company Research and Technicals",
    instructions="""
    Use this tool for invoking a subagent for your company research and technicals. It researches stock prices, analyst recommendations, and stock fundamentals.
    """,
)
async def invoke_technical_subagent(query:str):

    settings = load_settings()
    model_implementation = OpenAIChat(
        id=settings["openrouter_model"],
        api_key=settings["openrouter_api_key"],
        base_url="https://openrouter.ai/api/v1",
        timeout=60,
        max_retries=1,
    )
    
    technical_subagent = Agent(
        name="Technical Subagent",
        tools=[YFinanceTools(all=True)],
        model=model_implementation,
        tool_call_limit=10,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=["Format your response using markdown and use tables to display data where possible.",],
    )

    result = await technical_subagent.arun(query)
    return result
