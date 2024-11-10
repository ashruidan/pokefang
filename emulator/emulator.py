import logging
from pyboy import PyBoy
from config import *

logging.basicConfig(level=logging.INFO)

MEMORY_MENU_X = 0xCC25
MEMORY_MENU_SELECTED = 0xCC26 
MEMORY_FLAG_EVENT_BEGIN = 0xD747
MEMORY_FLAG_EVENT_END = 0xD87E

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

    def retrieve_memory(self, addr):
        return self.pyboy.memory[addr]

    def event_flags(self):
        return sum([
            int.bit_count(self.retrieve_memory(addr))
            for addr in range(MEMORY_FLAG_EVENT_BEGIN, MEMORY_FLAG_EVENT_END)
        ])

    def battle_menu(self):
        return (
            self.retrieve_memory(MEMORY_MENU_X),
            self.retrieve_memory(MEMORY_MENU_SELECTED)
        )
