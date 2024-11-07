import random, logging
from pyboy import PyBoy
from agent.agent import agent_move
from config import *

logging.basicConfig(level=logging.INFO)

class Emulator:
    def __init__(self):
        self.pyboy = PyBoy(ROM_PATH)
        if not self.pyboy:
            raise RuntimeError("Failed to initialize PyBoy with the given ROM.")
        self.pyboy.set_emulation_speed(EMULATION_SPEED)
        logging.info("Emulator initialized with ROM : %s", ROM_PATH)

    def load_state(self, state_path=START_SAVE_PATH):
        with open(state_path, "rb") as path:
            self.pyboy.load_state(path)
        logging.info("Game state loaded from %s", state_path)

    def controller_input(self, input):
        self.pyboy.button_press(input)
        self.pyboy.tick(HOLD_TICK)
        self.pyboy.button_release(input)
        self.pyboy.tick(RELEASE_TICK)

    def stop(self):
        self.pyboy.stop(False)
        logging.info("Emulator stopped.")

def run(isHuman):
    env = Emulator()
    env.load_state()
    done = False
    try:
        while not done:
            if not isHuman:
                env.controller_input(agent_move())
            env.pyboy.tick()
    except KeyboardInterrupt:
        print("Program interrupted. Stopping emulator...")
    finally:
        env.stop()
