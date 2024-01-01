from langchain.agents import Tool, tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools.base import StructuredTool

from calendar_functions import find_event_by_summary,get_events_on_date,create_event,today


class Today(BaseModel):
    n: int = Field()
    pass

class DateEvents(BaseModel):
    target_date: str = Field()
    pass
class SummaryEvent(BaseModel):
    summary: str = Field()
    pass

class EventCreator(BaseModel):
    meeting_name:str = Field()
    description:str = Field()
    start_time:str = Field()
    end_time:str = Field()
    location:str = Field()
    attendees:str = Field()
    reminders:str = Field()


get_events_on_date=Tool(
    name='get_events_on_date',
    func=get_events_on_date,
    description="Used to get the meeting details of a specific date. input is the date in the format 2023-MM-DD",
    args_schema=DateEvents,
)



find_event_by_summary= Tool(
    name='find_event_by_summary',
    func=find_event_by_summary,
    description="Used to find a meeting or event on calendar. input is the meeting name",
    args_schema=SummaryEvent,
)

create_event= StructuredTool(
    name='create_event',
    func=create_event,
    description="Used to create a new event use time format (YYYY-MM-DDTHH:MM:SS) and if any value is missing pass None",
    args_schema=EventCreator,
)


today=Tool(
    name='today',
    func=today,
    description="Used to get the date for today. please use it first before using anything else. the function has no input argument",
    args_schema=Today,
)
tools =[find_event_by_summary,get_events_on_date,create_event,today]
