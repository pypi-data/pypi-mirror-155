
# tomato-engine

**Engine for prototyping and playing with cellular automata.**

## Motivation

Tomato-engine aims to be an easy to use, extensible and hackable
framework for running cellular automata simulations controlled
via Python.

It handles much of the overhead involved in getting a simple
 realtime visualization of the cellular automata to run, while
 providing an object oriented interface through which the user
 can easily craft their own cellular automata ruleset, and leave
 tomato-engine to handle all the rest.

## Installation

```
pip3 install tomato-engine
```

## Example and basic usage

New rules are implemented on a Python module, which must contain
the class Cell, which inherits from CellTemplate and specifies
how the cell should update on each iteration through the function
Cell.update.

For simple, binary automata rulesets such as the Conway's Game of
Life, the class can be as simple as this:

```python
from tomato.classes import cell

class Cell(cell.CellTemplate):
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell
        if self.value == 0:
            if self.live_neighbors == 3:
                self.value = 1
            else:
                self.value = 0
        # Live cell
        else:
            if self.live_neighbors in (2, 3):
                self.value = 1
            else:
                self.value = 0

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_neighbors(self):
        return sum(self.neighbors)
```

This module is then imported and passed to the Board class, which
provides the user interface. 

```python
import tomato as tt
from tomato.functions import utils

from my_rules import game_of_life as rule

# Board dimensions in number of automata in each direction
board_dimensions = (100, 100)

# Scaling factor for the board in the display
cell_size = 4

# Convenience function for generating a numpy matrix
# of random binary values
state_matrix = utils.random_matrix(board_dimensions, 2)

board = tt.Board(rule, cell_size=cell_size)

# Opens the simulation window
board.start(state_matrix)
```

Also check out our [repository of rulesets](https://codeberg.org/CSL.dev/tomato-rules)
made for tomato-engine.

More information on how to craft new rulesets and interact with
your simulation can be found on our readthedocs: (coming soon!)
