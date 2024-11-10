from agent.agent import Agent
from config import EPISODE_SIZE, BATCH_SIZE
from .emulator import Emulator
from .global_map import local_to_global

#MEMORY_EXPLORATION_TYPE = 0xFFD7 [0 = Indoor, 1 = Special, 2 = Outside/Oak Lab]
MEMORY_BATTLE_TYPE = 0xD057 # [0 = No, 1 = Wild, 2 = Trainer] Battle
MEMORY_LOCAL_Y = 0xD361
MEMORY_LOCAL_X = 0xD362
MEMORY_LOCAL_MAP = 0xD35E

def run(mode):
    agent = Agent()
    env = Emulator(headless=mode.headless)
    env.load_state()
    try:
        if mode.human or mode.eval:
            episode(env, agent, mode.human,-1)
        else:
            batch(env, agent, mode.human)
    except KeyboardInterrupt:
        print("Program interrupted. Stopping emulator...")
    finally:
        del agent
        env.stop()

def batch(env, agent, human, batch_size=BATCH_SIZE):
    while batch_size:
        episode(env, agent, human)
        env.load_state()
        batch_size -= 1

def episode(env, agent, human, episode_size=EPISODE_SIZE):
    done = False
    while not done and episode_size:
        local_y = env.retrieve_memory(MEMORY_LOCAL_Y)
        local_x = env.retrieve_memory(MEMORY_LOCAL_X)
        local_map = env.retrieve_memory(MEMORY_LOCAL_MAP)
        state = {
            "step_left": episode_size,
            "battle": env.retrieve_memory(MEMORY_BATTLE_TYPE),
            "position": local_to_global(local_y, local_x, local_map),
            "events": env.event_flags(),
            "battle_menu": env.battle_menu(),
        }
        if not human:
            env.controller_input(agent.step(state, episode_size != -1))
        else:
            agent.algo.qtable_print(state)
        env.pyboy.tick()
        if episode_size != -1:
            episode_size -= 1


