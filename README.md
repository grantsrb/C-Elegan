# C-Elegan

## Description
C-Elegan is a multi-agent, descretized simulation of a [c-elegan's](https://en.wikipedia.org/wiki/Caenorhabditis_elegans) natural environment made as an OpenAI gym environment.

## Dependencies
- pip
- gym
- numpy
- matplotlib

## Installation
1. Clone this repository
2. Navigate to the cloned repository
3. Run command `$ pip install -e ./`

## Using C-Elegan

#### CEleganEnv
Use `gym.make('CElegan-v0')` to make a new environment with the following default options (see Game Details to understand what each variable does):

    grid_size = [15,15]
    unit_size = 10
    unit_gap = 1
    elegan_size = 3
    n_elegans = 1
    n_foods = 1

## Game Details
#### Observations
Each observation consists of the gradient of the distance from the food in the spaces to the right and left of the elegan's head. This means that the observation space is a vector of length 2. Each c-elegan receives a unique observation vector.

The gradient from the food is equivalent to 1/(distance from food)^2

#### Rewards
A +1 reward is returned when a elegan eats a food.

A -1 reward is returned when a elegan dies.

No extra reward is given for victory elegans in plural play.

#### Game Options

- _grid_size_ - An x,y coordinate denoting the number of units on the elegan grid (width, height).
- _unit_size_ - Number of numpy pixels within a single grid unit.
- _unit_gap_ - Number of pixels separating each unit of the grid. Space between the units can be useful to understand the direction of the elegan's body.
- _elegan_size_ - Number of body units for each elegan at start of game
- _n_elegans_ - Number of individual elegans on grid
- _n_foods_ - Number of food units (the stuff that makes the elegans grow) on the grid at any given time.

Each of these options are member variables of the environment and will come into effect after the environment is reset. For example, if you wanted to use 5 food tokens in the regular version, you can be set the number of food tokens using the following code:

    env = gym.elegan('elegan-v0')
    env.n_foods = 5
    observation = env.reset()

This will create a vanilla elegan environment with 5 food tokens on the map.


#### General Info
The elegan environment has three main interacting classes to construct the environment. The three are a Snake class, a Grid class, and a Controller class. Each holds information about the environment, and each can be accessed through the gym environment.

    import gym
    import c_elegan

    # Construct Environment
    env = gym.make('Elegan-v0')
    observation = env.reset() # Constructs an instance of the game

    # Controller
    game_controller = env.controller

    # Grid
    grid_object = game_controller.grid
    grid_pixels = grid_object.grid

    # Snake(s)
    elegans_array = game_controller.elegans
    elegan_object1 = elegans[0]

#### Using Multiple Snakes
Snakes can be distinguished by the Green value of their `head_color` attribute. Each head color consists of [Red=255, Green=uniqueNonZeroValue, Blue=0]. For each elegan instantiated, the head color will corespond to its index within the controller's elegan array. The head value will take on [255, (i+1)*10, 0] where i is the index of the elegan.

When using multiple elegans, at each step, you pass an array of actions corresponding to the action of each elegan. The return is an array of rewards corresponding each elegan. The reward returned upon a elegans' death is -1, each subsequent step after this, however, is a reward of 0. The contents of the action array are ignored at a dead elegan's index, the action array must, however, continue to have an index for each elegan that originally started out the game.

#### Coordinates
The units of the game are made to take up multiple pixels within the grid. Each unit has an x,y coordinate associated with it where (0,0) represents the uppermost left unit of the grid and (`grid_object.grid_size[0]`, `grid_object.grid_size[1]`) denotes the lowermost right unit of the grid. Positional information about elegan food and elegans' bodies is encoded using this coordinate system.

#### Snake Class
This class holds all pertinent information about an individual elegan. Useful information includes:

    # Action constants denote the action space.
    elegan_object1.UP # Equal to integer 0
    elegan_object1.RIGHT # Equal to integer 1
    elegan_object1.DOWN # Equal to integer 2
    elegan_object1.LEFT # Equal to integer 3

    # Member Variables
    elegan_object1.direction # Indicates which direction the elegan's head is pointing; initially points DOWN
    elegan_object1.head # x,y Coordinate of the elegan's head
    elegan_object1.head_color # A pixel ([R,G,B]) of type uint8 with an R value of 255
    elegan_object1.body # deque containing the coordinates of the elegan's body ordered from tail to neck [furthest from head, ..., closest to head]

#### Grid Class
This class holds all pertinent information about the grid that the elegans move on. Useful information includes:

    # Color constants give information about the colors of the grid
    # Each are ndarrays with dtype uint8
    grid_object.BODY_COLOR # [1,0,0] Color of elegan body units
    grid_object.HEAD_COLOR # [255, (i+1)*10, 0] Color of elegan head units. i is the index of the elegan.
    grid_object.FOOD_COLOR # [0,0,255] Color of food units
    grid_object.SPACE_COLOR # [0,255,0] Color of blank space

    # Member Variables
    grid_object.unit_size # See Game Options
    grid_object.unit_gap # See Game Options
    grid_object.grid_size # See Game Options
    grid_object.grid # Numpy [R,G,B] pixel array of game

#### Controller Class
The Controller holds a grid object and an array of elegans that move on the grid. The Controller class handles the game logic between the elegans and the grid. Actions are taken through this class and initialization parameters within this class dictate the initial parameters of the grid and elegan objects in the game. Useful information includes:

    # Member variables
    game_controller.grid # An instance of the grid class for the game
    self.elegans # An array of elegan objects that are on the board. If a elegan dies, it is erased and it becomes None.
