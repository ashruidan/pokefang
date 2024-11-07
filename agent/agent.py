import random
from emulator.actions import Actions

def agent_move():
    action = random.choice(Actions.list())
    return action

