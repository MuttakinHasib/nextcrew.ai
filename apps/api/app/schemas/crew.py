from pydantic import BaseModel


class RunCrew(BaseModel):
    companies: list[str]
    positions: list[str]
