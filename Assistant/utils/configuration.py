# This file contains all the configuration variables that we will require to access throughout our agent 

import os 
from dataclasses import dataclass , field , fields
from typing import Any , Optional

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated

# We will be using dataclasses decorator to define our Configuration class
@dataclass(kw_only=True)
class Configuration:
    """ This class contains the configuration fields that are required for the chatbot."""
    
    user_id : str = "default_user"
    todo_category : str = "general"
    task_maistro_role : str = "You are a task management personal assistant. You role is to help the user create , organize and manage their tasks using a ToDo list."

    @classmethod
    def from_runnable_config(
        cls, 
        config:Optional[RunnableConfig] = None
    ) -> "Configuration":
        
        """ Here we will be using the RunnableConfig to create the Configuration instance."""

        
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # This extracts the final values for the configuration fields(e.g. user_id, todo_category, etc.) at run time.
        values : dict[str , Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v is not None})
