## This file contains all the nodes definitions for our agent 

# Imports 
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from trustcall import create_extractor

from typing import Literal, Optional, TypedDict

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import merge_message_runs
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
import configuration

## Defining the node for the mAIstro agent
def task_mAIstro(state:MessagesState , config: RunnableConfig, store: BaseStore):
    """Load memories from the store and use them to personalize the chatbot's responses."""

    # Get the user ID from the config
    configurable = configuration.Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    todo_category = configurable.todo_category

    # define the namespace for the memory
    namespace = ("profile", todo_category, user_id)

    # retrieve the memories from the store
    existing_items = store.search(namespace)

    # format the existing memories for the trustcall extractor
    tool_name = "Profile" 
    existing_memories = (
    [
    (existing_items.key, tool_name, existing_items.value) 
    for existing_items in existing_items
    ]
    if existing_items
    else None
    )

