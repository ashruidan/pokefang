# pokefang from Pokemon-Tonail

## Introduction

Implementing a Q-learning algorithm to train an agent to play Pokemon Red.

>[!WARNING]
>The project is now deprecated; please refer to its continuation under the new project, [daikonquest](https://github.com/ashruidan/daikonquest)."

## Requirements 

(not showing their dependencies)

- Python >= 3.13
- numpy  >= 2.1.3
- pyboy  ~= 2.4.0

## Running the project

`python main.py (--headless | --human | --eval | --train)`

Use the commands with one of the following arguments :
- --headless  To train with no graphical output
- --human     To debug manually
- --train     To train while visualizing
- --eval      To see the evolution of the Q Table

Note 1 : Parallel not implemented
Note 2 : Checkpoint save not implemented

## File Structure

### Root Project

- main.py          : Parsing argument and running the project
- config.py        : Contains paths and hyperparameters
- requirements.txt : List of required Python packages for pip
- pixi.toml        : List of required Python packages for pixi

### Emulator Folder

- emulator.py      : Interface between PyBoy and the project 
- environment.py   : Normalize running session
- actions.py       : Enumeration of possible actions
- global_map.py    : Convert local position to global position
- bw_squirtle.save : Starting save for the AI, just after Rival Fight
- events.json      : Most of the event flags in Pokemon Red
- map_data.json    : Data for the conversion local to global

### Agent Folder

- agent.py         : Decision making of the agent
- qlearning.py     : Algorithm used by agent to make decision and to learn
- qtable.pkl       : Lookup table for Q Learning Algorithm

## Result

The agent learns over time and improves its performance based on rewards from event flags triggered in the game.
It has no difficulty to find the closest reward, but need more time and control on hyperparameter to get into further rewards.

One of the problem encountered is the fact that the Q-Learning algorithm is not optimal when scaling from the beginning of the game to the goal of finishing the game.

## Follow-up

Because of the non scalability of Q Learning, I plan to transition to Deep Q-Learning which will use a neural network in place of the lookup table.
