from textwrap import dedent
from crewai import Task, Agent


class CompanyResearchTasks:
    def __init__(self, job_id: str):
        self.job_id = job_id

    def manager_research(
        self,
        agent: Agent,
        companies: list[str],
        positions: list[str],
        tasks: list[Task],
    ) -> Task:
        return Task(
            description=dedent(
                f"""Based on the list of companies {companies} and the positions {positions},
                use the results from the Company Research Agent to research each position in each company.
                to put together a json object containing the URLs for 3 blog articles, the URLs and title
                for 3 YouTube interviews for each position in each company.

                """,
            ),
            agent=agent,
            expected_output=dedent(
                """A json object containing the URLs for 3 blog articles and the URLs and
                    titles for 3 YouTube interviews for each position in each company.
                """
            ),
            callback=self.append_event_callback,
            context=tasks,
            output_json=PositionInfoList,
        )

    def company_research(self):
        pass
