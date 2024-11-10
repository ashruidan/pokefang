import random, numpy as np
from emulator.actions import Actions

DEFAULT_EVENT_COUNT = 6

class QLearning:
    def __init__(self, load):
        self.previous_state = None
        self.previous_action = None
        if load == None:
            self.qtable = np.full((10,500,500,len(Actions.list())),-1.)
            self.episode_count = 0
            self.steps_exploration = 0
            self.steps_battle = 0
            self.event_max = 6
        else:
            self.qtable = load["qtable"]
            self.episode_count = load["episode_count"]
            self.steps_exploration = load["steps_exploration"]
            self.steps_battle = load["steps_battle"]
            self.event_max = load["event_max"]
    def stop(self):
        save = {
            "qtable": self.qtable,
            "episode_count": self.episode_count,
            "steps_exploration": self.steps_exploration,
            "steps_battle": self.steps_battle,
            "event_max": self.event_max,
        }
        return save

    def step_battle(self, battle_menu):
        flag = self.previous_state["battle_menu"] == battle_menu and self.previous_action == Actions.DOWN.value
        if battle_menu == (9,1):
            action = Actions.RIGHT.value
        elif battle_menu == (15,1) or flag:
            action = Actions.A.value
        else:
            action = Actions.DOWN.value
        return action

    def step(self, state, train):
        if state["battle"]:
            action = self.step_battle(state["battle_menu"])
        else:
            qtable_action = self.qtable_action(state)
            if train and self.epsilon(state["events"]):
                action = random.choice(Actions.list())
            else:
                action = qtable_action
            if train and self.previous_state != None:
                self.qtable_update(state, qtable_action)
        self.previous_action = action
        self.previous_state = state
        return action

    def qtable_update(self, state, qtable_action):
        lr = 0.1 # learning rate
        g = 0.9 # gamma or discount factor
        r = (state["events"] - self.previous_state["events"])
        r *= 1000 * state["events"] # Reward Bump
        prev_y, prev_x = self.previous_state["position"]
        prev_e = self.previous_state["events"] - DEFAULT_EVENT_COUNT
        prev_action = Actions.list().index(self.previous_action)
        y,x = state["position"]
        e = state["events"] - DEFAULT_EVENT_COUNT
        action = Actions.list().index(qtable_action)
        best_action = self.qtable[e,y,x,action]
        prev_r = self.qtable[prev_e,prev_y,prev_x,prev_action]
        self.qtable[prev_e,prev_y,prev_x,prev_action] += lr*(r+g*best_action-prev_r)

    def qtable_action(self, state):
        y, x = state["position"]
        e = state["events"] - DEFAULT_EVENT_COUNT
        actions = self.qtable[e,y,x,:]
        index = np.argmax(actions)
        return Actions.list()[index]

    def epsilon(self, event_current):
        self.event_max = max(self.event_max, event_current)
        epsilon = event_current / self.event_max
        return np.random.random() < epsilon

    def qtable_print(self, state):
        y, x = state["position"]
        e = state["events"] - 6
        actions = self.qtable[e,y,x,:]
        index = np.argmax(actions)
        print(f"ev:{state["events"]}/{self.event_max}, Action={Actions.list()[index]}:{np.max(actions)}, List={actions}")
