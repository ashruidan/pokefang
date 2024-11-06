import random
from agent.actions import Actions

def agent_move():
    action = random.choice(Actions.list())
    return action
