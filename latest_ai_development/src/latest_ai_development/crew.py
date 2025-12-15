from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
import os


@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def military_strategy_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['military_strategy_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )


    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def military_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['military_analysis_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
       
        # Configure LLM for OpenRouter - Using GPT-4o-mini via OpenRouter
        # Model format: openai/gpt-4o-mini (OpenRouter format)
        # CrewAI will use OPENAI_API_KEY and OPENAI_API_BASE from .env
        model_name = os.getenv("MODEL", "openai/gpt-4o-mini")
        llm = LLM(model=model_name)

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            llm=llm,  # Use the configured LLM
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
