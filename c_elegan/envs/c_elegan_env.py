import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from c_elegan.envs.elegan import Controller, Discrete

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class CEleganEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, grid_size=[15,15], unit_size=10, unit_gap=1, n_elegans=1, n_foods=1):
        self.grid_size = grid_size
        self.unit_size = unit_size
        self.unit_gap = unit_gap
        self.n_elegans = n_elegans
        self.n_foods = n_foods
        self.viewer = None
        self.action_space = Discrete(3)

    def _step(self, action):
        return self.controller.step(action)

    def _reset(self):
        self.controller = Controller(self.grid_size, self.unit_size, self.unit_gap, self.n_elegans, self.n_foods)
        return self.controller.get_obses()

    def _render(self, mode='human', close=False):
        obs = self.controller.grid.draw_elegans(self.controller.elegans)
        if self.viewer is None:
            self.viewer = plt.imshow(obs)
        else:
            self.viewer.set_data(obs)
        plt.pause(0.1)
        plt.draw()

    def _seed(self, x):
        pass
