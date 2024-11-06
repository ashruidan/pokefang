import random
from agent.agent import agent_move
from emulator.game_controller import GameController
from config import ROM_PATH, EMULATION_SPEED

def run(isHuman):
    env = GameController(ROM_PATH, EMULATION_SPEED)
    env.load_state()
    done = False
    try:
        while not done:
            if not isHuman:
                env.perform_action(agent_move())
            env.pyboy.tick()
    except KeyboardInterrupt:
        print("Program interrupted. Stopping emulator...")
    finally:
        env.close()
