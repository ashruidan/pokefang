import os, random, pickle, numpy as np
from emulator.actions import Actions
from .qlearning import QLearning

PATH_AGENT_QTABLE = "agent/qtable.pkl"

class Agent:
    def __init__(self):
        load = None
        if os.path.exists(PATH_AGENT_QTABLE):
            with open(PATH_AGENT_QTABLE, "rb") as file:
                load = pickle.load(file)
        self.algo = QLearning(load)

    def __del__(self):
        save = self.algo.stop()
        with open(PATH_AGENT_QTABLE, "wb") as file:
            pickle.dump(save, file)

    def step(self, state, train):
        return self.algo.step(state, train)
