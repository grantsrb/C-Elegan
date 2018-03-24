from c_elegan.envs.elegan import CElegan
from c_elegan.envs.elegan import Grid
import numpy as np

class Controller():
    """
    This class combines the Snake, Food, and Grid classes to handle the game logic.
    """

    def __init__(self, grid_size=[30,30], unit_size=10, unit_gap=1, n_elegans=1, n_foods=1):

        assert n_elegans < grid_size[0]//3
        assert n_elegans < 25
        assert 4 < grid_size[1]//2
        assert unit_gap >= 0 and unit_gap < unit_size

        self.elegans_remaining = n_elegans
        self.grid = Grid(grid_size, unit_size, unit_gap)

        self.elegans = []
        self.dead_elegans = []
        for i in range(1,n_elegans+1):
            start_coord = [i*grid_size[0]//(n_elegans+1), 4]
            self.elegans.append(CElegan(start_coord))
            self.elegans[-1].head_color = -i
            self.dead_elegans.append(None)

        for i in range(n_foods):
            self.grid.new_food()

    def get_obses(self):
        """
        Finds the observations for each elegan
        """
        if len(self.elegans) == 1:
            return self.grid.get_obs(self.elegans[0])
        else:
            obses = []
            for i in range(len(self.elegans)):
                obses.append(self.grid.get_obs(self.elegans[i]))
            return obses

    def move_elegan(self, direction, elegan_idx):
        """
        Moves the specified elegan according to the game's rules dependent on the direction.
        Does not draw head and does not check for reward scenarios. See move_result for these
        functionalities.

        direction - integer between 0 and 3, actions are relative to elegan's direction:
                0 - left
                1 - straight
                2 - right
        """

        elegan = self.elegans[elegan_idx]
        if type(elegan) == type(None):
            return

        # Find and set next head position conditioned on direction
        elegan.action(direction)

    def move_result(self, direction, elegan_idx=0):
        """
        Checks for food and death collisions after moving elegan. Draws head of elegan if
        no death scenarios.
        """

        elegan = self.elegans[elegan_idx]
        if type(elegan) == type(None):
            return 0

        # Check for death of elegan
        if self.grid.check_death(elegan.head):
            self.dead_elegans[elegan_idx] = self.elegans[elegan_idx]
            self.elegans[elegan_idx] = None
            reward = -1
        # Check for reward
        elif self.grid.food_space(elegan.head):
            reward = 1
            self.grid.new_food()
        else:
            reward = 0

        return reward

    def kill_elegan(self, elegan_idx):
        """
        Deletes elegan from game and subtracts from the elegan_count 
        """
        
        assert self.dead_elegans[elegan_idx] is not None
        self.dead_elegans[elegan_idx] = None
        self.elegans_remaining -= 1

    def step(self, directions):
        """
        Takes an action for each elegan in the specified direction and collects their rewards
        and dones.

        directions - tuple, list, or ndarray of directions corresponding to each elegan.
                    If single elegan, int direction is okay
        """

        # Ensure no more play until reset
        if self.elegans_remaining < 1:
            if len(directions) is 1:
                return self.grid.null_obs(), 0, True, {"elegans_remaining":self.elegans_remaining}
            else:
                obses = []
                for i in range(len(self.elegans):
                    obses.append(self.grid.null_obs())
                return obses, [0]*len(directions), True, {"elegans_remaining":self.elegans_remaining}

        rewards = []

        if type(directions) == type(int()):
            directions = [directions]

        for i, direction in enumerate(directions):
            if self.elegans[i] is None and self.dead_elegans[i] is not None:
                self.kill_elegan(i)
            self.move_elegan(direction,i)
            rewards.append(self.move_result(direction, i))

        done = self.elegans_remaining < 1
        if len(rewards) is 1:
            return self.get_obses(), rewards[0], done, {"elegans_remaining":self.elegans_remaining}
        else:
            return self.get_obses(), [0]*len(directions), done, {"elegans_remaining":self.elegans_remaining}
