import logging
from pyboy import PyBoy
from emulator.global_map import local_to_global

logging.basicConfig(level=logging.INFO)


class GameController:
    def __init__(self, rom_path, emulation_speed=1.0):
        self.pyboy = PyBoy(rom_path)
        if not self.pyboy:
            raise RuntimeError("Failed to initialize PyBoy with the given ROM.")

        self.pyboy.set_emulation_speed(emulation_speed)
        logging.info("GameController initialized with ROM: %s", rom_path)

    def save_state(self, state_filename="game_state.save"):
        with open(state_filename, "wb") as f:
            self.pyboy.save_state(f)
        logging.info("Game state saved to %s", state_filename)

    def load_state(self, state_filename="squirt_two.save"):
        with open(state_filename, "rb") as f:
            self.pyboy.load_state(f)
        logging.info("Game state loaded from %s", state_filename)
        print(f" the coords are {self.get_game_coords()}")

    def close(self):
        self.pyboy.stop()
        logging.info("Emulator stopped.")

    # implement the locatin
    # x_pos = self.pyboy.get_memory_value(0xD361)
    # y_pos = self.pyboy.get_memory_value(0xD362)
    # map_n = self.pyboy.get_memory_value(0xD35E)

    def get_game_coords(self):
        return (self.read_m(0xD362), self.read_m(0xD361), self.read_m(0xD35E))

    def read_m(self, addr):
        # return self.pyboy.get_memory_value(addr)
        return self.pyboy.memory[addr]

    def get_global_coords(self):
        x_pos, y_pos, map_n = self.get_game_coords()
        return local_to_global(y_pos, x_pos, map_n)

    def is_in_battle(self):
        """Returns True if the game is currently in a battle."""
        # Memory address 0xD057 indicates battle state
        battle_type = self.read_m(0xD057)

        # if battle_type:
        #     print("in battle!")
        return battle_type != 0

    def perform_action(self, action):
        action_map = {
            "A": "a",
            "B": "b",
            "START": "start",
            "SELECT": "select",
            "UP": "up",
            "DOWN": "down",
            "LEFT": "left",
            "RIGHT": "right",
        }

        if action in action_map:
            button = action_map[action]
            self._press_button(button, hold_ticks=20, release_ticks=2)
            #logging.info("Performed action: %s", action)
        else:
            raise ValueError(f"Unknown action: {action}")

    def _press_button(self, button, hold_ticks=20, release_ticks=2):
        """Helper method to press and release a button with specified ticks."""
        self.pyboy.button_press(button)
        self.pyboy.tick(hold_ticks)
        self.pyboy.button_release(button)
        self.pyboy.tick(release_ticks)

    def update(self):
        """Retrieve the current state of the game."""
        # Replace with actual game state retrieval logic
        state = {}  # Example placeholder for game state
        logging.info("Game state updated.")
        return state
