from app.core.job_manager import append_event


class CompanyResearcherCrew:
    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.crew = None

    def setup_crew(self, companies: list[str], positions: list[str]) -> None:
        print(
            f"Setting up crew for {self.job_id} with companies {companies} and positions {positions}"
        )
        # TODO: SETUP AGENTS
        # TODO: SETUP TASKS
        # TODO: CREATE CREW

    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.job_id}")
            return

        append_event(self.job_id, "CREW STARTED")

        try:
            print(f"Running crew for {self.job_id}")

            results = self.crew.kickoff()
            append_event(self.job_id, "CREW COMPLETED")
            return results

        except Exception as e:
            print(f"Error running crew for {self.job_id}")
            return str(e)
