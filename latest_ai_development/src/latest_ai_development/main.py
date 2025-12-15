#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from latest_ai_development.crew import LatestAiDevelopment

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ============================================
# LANGFUSE OBSERVABILITY SETUP
# ============================================
# Initialize Langfuse for tracing and monitoring CrewAI agents
# Credentials are loaded from environment variables:
# - LANGFUSE_SECRET_KEY
# - LANGFUSE_PUBLIC_KEY  
# - LANGFUSE_BASE_URL
from langfuse import get_client
from openinference.instrumentation.crewai import CrewAIInstrumentor

# Initialize Langfuse client
langfuse = get_client()

# Initialize CrewAI instrumentation for automatic tracing
CrewAIInstrumentor().instrument(skip_dep_check=True)

# Verify Langfuse connection
if langfuse.auth_check():
    print("✅ Langfuse observability is enabled and connected!")
else:
    print("⚠️  Langfuse authentication failed. Check your API keys.")

# ============================================

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with Langfuse observability.
    """
    inputs = {
        'topic': 'World war 1',
    }

    try:
        # Wrap crew execution with Langfuse tracing span
        with langfuse.start_as_current_observation(
            as_type="span",
            name="crewai-world-war-1-research",
            metadata={
                "topic": inputs['topic'],
                "crew": "LatestAiDevelopment",
                "user": "Nasrallah Hasan"
            }
        ) as span:
            result = LatestAiDevelopment().crew().kickoff(inputs=inputs)
            
            # Update trace with output
            span.update_trace(
                input=str(inputs),
                output=str(result) if result else "No output"
            )
            
        # Flush traces to ensure they're sent
        langfuse.flush()
        print("✅ Traces sent to Langfuse successfully!")
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        LatestAiDevelopment().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopment().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "World war 1",
        "current_year": str(datetime.now().year)
    }

    try:
        LatestAiDevelopment().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = LatestAiDevelopment().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
