## This file contains all the schema definition for our assistant

# Imports 
from pydantic import BaseModel , Field
from typing import Optional , List , Dict , TypedDict, Literal
from datetime import datetime


# Defining User Profile Schema
class Profile(BaseModel):

    """ This is the profile schema for the user. It contains the user's name, age , location and job and interests."""

    name: Optional[str] = Field(description="The user's name" , default=None)
    age: Optional[int] = Field(description="The user's age" , default=None)
    location: Optional[str] = Field(description="The user's location" , default=None)
    job: Optional[str] = Field(description="The user's job" , default=None)
    connections : list[str] = Field(description="Personal connections of the user such as family members , friends or coworkers" , default_factory=list)
    interests: Optional[List[str]] = Field(description="The user's interests" , default_factory=list)


# ToDo Schema 
class ToDo(BaseModel):
    """ This is the schema for the todo list and contains the task , time for completion , deadline , solutions and status of the task."""

    task: str = Field(description = "The task to be completed")
    time_to_complete: Optional[int] = Field(description="Estimated time to complete the task (minutes)")
    deadline: Optional[datetime] = Field(desctiption =" In what time the task needs to be completed(if applicable)",
                                         default=None)
    solutions: Optional[List[str]] = Field(
        description="List of specific , actionable solutions (e.g. , specific ideas , service providers , or concrete options relevant to completing the task)" , 
        default_factory=list
    )
    status : Literal["not started" , "in progress", "done" , "archived" , "dropped"] = Field(
        description="The status of the task" , 
        default="not started"
    )
