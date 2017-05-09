# Utility classes and functions

#imports
from enum import Enum

class IdeaState(Enum):
    NEW = 0
    REVIEWED = 1
    IN_PROGRESS = 2
    DONE = 3


#TODO can this be made part of enum class?
# return states in a dictionary
def getStatesInDict():
    states = {
              IdeaState.NEW.value:IdeaState.NEW.name,
              IdeaState.REVIEWED.value:IdeaState.REVIEWED.name,
              IdeaState.IN_PROGRESS.value:IdeaState.IN_PROGRESS.name,
              IdeaState.DONE.value:IdeaState.DONE.name
             }
    return states
