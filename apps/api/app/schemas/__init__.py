from pydantic import BaseModel


class NameUrl(BaseModel):
    name: str
    url: str


class PositionInfo(BaseModel):
    company: str
    position: str
    name: str
    blog_articles_urls: list[str]
    youtube_interviews_urls: list[NameUrl]


class PositionInfoList(BaseModel):
    positions: list[PositionInfo]
