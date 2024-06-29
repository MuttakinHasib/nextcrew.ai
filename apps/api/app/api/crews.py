from datetime import datetime
from threading import Thread
from uuid import uuid4
from fastapi import APIRouter


from app.core.crewai import CompanyResearchCrew
from app.core.job_manager import append_event, jobs_lock, jobs, Event
from app.schemas.crew import RunCrew


router = APIRouter(prefix="/crews", tags=["Crews"])


def kickoff_crew(job_id, companies: list[str], positions: list[str]):
    print(f"Crew for job {job_id} is starting")

    results = None
    try:
        company_research_crew = CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(companies, positions)
        results = company_research_crew.kickoff()
        print(f"Crew for job {job_id} is complete", results)

    except Exception as e:
        print(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = "COMPLETE"
        jobs[job_id].result = results  # type: ignore
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete")
        )


@router.get("")
async def get_crews():
    return []


@router.post("")
async def run_crew(payload: RunCrew):
    job_id = str(uuid4())
    companies = payload.companies
    positions = payload.positions
    thread = Thread(
        target=kickoff_crew,
        args=(job_id, companies, positions),
    )

    thread.start()

    return {job_id}
