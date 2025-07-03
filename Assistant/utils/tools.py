## Here we initialize the tools that will be used by the agent.

# Imports
from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from trustcall import create_extractor
from .schema import Profile, ToDo
# Update memory tool 
class UpdateMemory(TypedDict):

    """ This tool is used to update the memory of the agent. It takes the decision on what memory to update."""

    update_type : Literal['user', 'todo' , 'instructions']

# initialize the model 

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0)

# Create the TrustCall extractor for updating the user profile, todo list
profile_extractor = create_extractor(
    model = model,
    tools = [Profile],
    tool_choice = "Profile"
)


    
