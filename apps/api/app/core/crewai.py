from datetime import datetime
from typing import Callable
from langchain_openai import ChatOpenAI

from app.configs.settings import settings
from app.core.agents import CompanyResearcherAgents

from app.core.job_manager import append_event

from crewai import Crew

from app.core.tasks import CompanyResearchTasks


class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

    def setup_crew(self, companies: list[str], positions: list[str]):
        agents = CompanyResearcherAgents()
        tasks = CompanyResearchTasks(job_id=self.job_id)

        research_manager = agents.research_manager(companies, positions)
        company_research_agent = agents.company_research_agent()

        company_research_tasks = [
            tasks.company_research(company_research_agent, company, positions)
            for company in companies
        ]

        manage_research_task = tasks.manager_research(
            research_manager, companies, positions, company_research_tasks
        )

        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_tasks, manage_research_task],
            verbose=2,
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)
