import random, logging, json
from pyboy import PyBoy
from agent.agent import agent_move
from config import *
from emulator.memory import memory

logging.basicConfig(level=logging.INFO)

class Emulator:
    def __init__(self, headless):
        self.pyboy = PyBoy(PATH_ROM, window="null" if headless else "SDL2")
        if not self.pyboy:
            raise RuntimeError("Failed to initialize PyBoy with the given ROM.")
        self.pyboy.set_emulation_speed(EMULATOR_SPEED_HEADLESS if headless else EMULATOR_SPEED_FULL)
        logging.info("Emulator initialized with ROM : %s", PATH_ROM)

    def load_state(self, state_path=PATH_START_SAVE):
        with open(state_path, "rb") as path:
            self.pyboy.load_state(path)
        logging.info("Game state loaded from %s", state_path)

    def controller_input(self, input):
        self.pyboy.button_press(input)
        self.pyboy.tick(EMULATOR_TICK_HOLD)
        self.pyboy.button_release(input)
        self.pyboy.tick(EMULATOR_TICK_RELEASE)

    def stop(self):
        self.pyboy.stop(False)
        logging.info("Emulator stopped.")

    def retrieve_mem(self, addresses):
        return {
            key: self.pyboy.memory[value]
            for key, value in addresses.items()
        }

def run(mode):
    env = Emulator(headless=mode.headless)
    env.load_state()
    try:
        if mode.human or mode.eval:
            episode(env, mode.human,-1)
        else:
            episode(env, mode.human)
    except KeyboardInterrupt:
        print("Program interrupted. Stopping emulator...")
    finally:
        env.stop()

def episode(env, human, episode_size=EPISODE_SIZE):
    done = False
    while not done and episode_size:
        if not human:
            env.controller_input(agent_move())
        env.pyboy.tick()
        if episode_size != -1:
            episode_size -= 1
