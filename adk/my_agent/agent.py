"""
Simple Google ADK Agent with Dummy Tools
=========================================
This is a demonstration agent built with Google's Agent Development Kit (ADK).
It includes dummy tools to showcase ADK's capabilities.
Uses OpenRouter API for model access.

Commands:
   adk web my_agent
   adk run my_agent
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm

# ============================================
# LOAD API KEY FROM ENVIRONMENT
# ============================================
# Load .env file from the adk directory
load_dotenv()

# Verify OpenRouter API key is set
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("⚠️  WARNING: OPENROUTER_API_KEY not found in environment!")
    print("   Create a .env file in the adk folder with:")
    print("   OPENROUTER_API_KEY=your-api-key-here")
    print("   Get your key at: https://openrouter.ai/keys")
else:
    print("✅ OpenRouter API Key loaded successfully!")


# ============================================
# DUMMY TOOLS
# ============================================

def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city to get weather for.
    
    Returns:
        A string describing the weather conditions.
    """
    # This is a dummy implementation
    weather_data = {
        "new york": "Sunny, 72°F (22°C)",
        "london": "Cloudy, 59°F (15°C)", 
        "tokyo": "Rainy, 68°F (20°C)",
        "paris": "Partly cloudy, 65°F (18°C)",
        "sydney": "Clear, 77°F (25°C)",
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city}: {weather_data[city_lower]}"
    return f"Weather in {city}: Mild, 70°F (21°C) - (simulated data)"


def calculate_math(expression: str) -> str:
    """
    Perform a simple math calculation.
    
    Args:
        expression: A math expression to evaluate (e.g., "2 + 2", "10 * 5").
    
    Returns:
        The result of the calculation as a string.
    """
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/.(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations are allowed (+, -, *, /)"
        result = eval(expression)
        return f"Result: {expression} = {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


def get_time(timezone: str = "UTC") -> str:
    """
    Get the current time in a specified timezone.
    
    Args:
        timezone: The timezone to get time for (default: UTC).
    
    Returns:
        The current time as a string.
    """
    from datetime import datetime
    # Dummy implementation - just returns current local time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time ({timezone}): {current_time} (simulated)"


def search_knowledge(query: str) -> str:
    """
    Search a knowledge base for information.
    
    Args:
        query: The search query.
    
    Returns:
        Relevant information from the knowledge base.
    """
    # Dummy knowledge base
    knowledge = {
        "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "ai": "Artificial Intelligence (AI) is the simulation of human intelligence by machines.",
        "machine learning": "Machine Learning is a subset of AI that enables systems to learn from data.",
        "google adk": "Google ADK (Agent Development Kit) is an open-source framework for building AI agents.",
        "crewai": "CrewAI is a framework for orchestrating role-playing autonomous AI agents.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return f"Found: {value}"
    
    return f"No specific information found for '{query}'. Try asking about: Python, AI, Machine Learning, Google ADK, or CrewAI."


# ============================================
# CREATE TOOLS FROM FUNCTIONS
# ============================================

weather_tool = FunctionTool(func=get_weather)
math_tool = FunctionTool(func=calculate_math)
time_tool = FunctionTool(func=get_time)
search_tool = FunctionTool(func=search_knowledge)


# ============================================
# CONFIGURE OPENROUTER MODEL
# ============================================

# Use LiteLLM to connect to OpenRouter
# Set max_tokens to stay within credit limits
openrouter_model = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
    max_tokens=4096,  # Limit output tokens to stay within credits
)

# ============================================
# DEFINE THE ROOT AGENT
# ============================================

root_agent = Agent(
    name="demo_assistant",
    model=openrouter_model,  # Using OpenRouter via LiteLLM
    description="A helpful assistant with weather, math, time, and knowledge tools.",
    instruction="""You are a helpful AI assistant created with Google ADK.

You have access to the following tools:
1. get_weather - Get weather information for any city
2. calculate_math - Perform math calculations
3. get_time - Get the current time in any timezone
4. search_knowledge - Search for information about various topics

When a user asks a question:
- Use the appropriate tool to help them
- Be friendly and informative
- If you're not sure which tool to use, ask for clarification

Always provide clear and helpful responses!""",
    tools=[
        weather_tool,
        math_tool,
        time_tool,
        search_tool,
    ],
)

