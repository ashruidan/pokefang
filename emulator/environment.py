import random, logging, json
from pyboy import PyBoy
from agent.agent import agent_move
from config import *
from emulator.memory import memory

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

    def retrieve_mem(self, addresses):
        return {
            key: self.pyboy.memory[value]
            for key, value in addresses.items()
        }

def run(human):
    env = Emulator()
    env.load_state()
    episode(human)

def episode(human):
    done = False
    try:
        while not done:
            state = env.retrieve_mem(memory))
            if not human:
                env.controller_input(agent_move(state))
            print(state)
            env.pyboy.tick()
    except KeyboardInterrupt:
        print("Program interrupted. Stopping emulator...")
    finally:
        env.stop()

