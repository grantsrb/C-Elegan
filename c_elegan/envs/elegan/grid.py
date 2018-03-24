import numpy as np

class Grid():

    """
    This class contains all data related to the grid in which the game is contained.
    The information is stored as a numpy array of gradient values.
    The grid is treated as an [x,y] plane in which [0,0] is located at
    the upper left most pixel and [max_x, max_y] is located at the lower right most pixel.

    Note that it is assumed spaces that can kill a c-elegan have a non-zero value as their 0 channel.
    """

    ELEGAN_COLOR = -1.
    FOOD_COLOR = 1.
    SPACE_COLOR = 0

    def __init__(self, grid_size=[30,30], unit_size=10, unit_gap=1):
        """
        grid_size - tuple, list, or ndarray specifying number of atomic units in
                    both the x and y direction
        unit_size - integer denoting the atomic size of grid units in pixels
        """

        self.unit_size = int(unit_size)
        self.unit_gap = unit_gap
        self.grid_size = np.asarray(grid_size, dtype=np.int) # size in terms of units
        height = self.grid_size[1]*self.unit_size
        width = self.grid_size[0]*self.unit_size
        self.grid = np.zeros((height, width), dtype=np.float32)

    def check_death(self, head_coord):
        """
        Checks the grid to see if argued head_coord has collided with a death space (i.e. the wall)

        head_coord - x,y integer coordinates as a tuple, list, or ndarray
        """
        return self.off_grid(head_coord)

    def color_of(self, coord):
        """
        Returns the color of the specified coordinate

        coord - x,y integer coordinates as a float
        """

        return self.grid[int(coord[1]*self.unit_size), int(coord[0]*self.unit_size)]

    def draw(self, coord, color):
        """
        Colors a single space on the grid. Use erase if creating an empty space on the grid.
        This function is used like draw but without affecting the open_space count.

        coord - x,y integer coordinates as a tuple, list, or ndarray
        color - float color value
        """

        if self.off_grid(coord):
            return False
        x = int(coord[0]*self.unit_size)
        end_x = x+self.unit_size-self.unit_gap
        y = int(coord[1]*self.unit_size)
        end_y = y+self.unit_size-self.unit_gap
        self.grid[y:end_y, x:end_x] = color
        return True

    def draw_copy(self, grid, coord, color):
        """
        Draws to the given grid.
        """
        if self.off_grid(coord):
            return grid
        x = int(coord[0]*self.unit_size)
        end_x = x+self.unit_size-self.unit_gap
        y = int(coord[1]*self.unit_size)
        end_y = y+self.unit_size-self.unit_gap
        grid[y:end_y, x:end_x] = color
        return grid

    def draw_elegans(self, elegans):
        """
        Returns a copy of the grid with the elgan bodies drawn with color ELEGAN_COLOR
        """
        grid_copy = self.grid.copy()
        for elegan in elegans:
            grid_copy = self.draw_elegan(grid_copy, elegan)
        return grid_copy

    def draw_elegan(self, grid, elegan):
        """
        Draws the elegan's head and body to the given grid.
        """
        grid = self.draw_copy(grid, elegan.head, elegan.head_color)
        for bod in elegan.body:
            grid = self.draw_copy(grid, bod, elegan.head_color)
        return grid

    def erase(self, coord):
        """
        Colors the entire coordinate with SPACE_COLOR to erase potential
        connection lines.

        coord - (x,y) as tuple, list, or ndarray
        """
        if self.off_grid(coord):
            return False
        self.open_space += 1
        x = int(coord[0]*self.unit_size)
        end_x = x+self.unit_size
        y = int(coord[1]*self.unit_size)
        end_y = y+self.unit_size
        self.grid[y:end_y, x:end_x] = self.SPACE_COLOR
        return True

    def new_food(self):
        """
        Draws a food on a random, open unit of the grid.
        """
        coord_not_found = True
        while(coord_not_found):
            coord = (np.random.randint(0,self.grid_size[0]), np.random.randint(0,self.grid_size[1]))
            if np.array_equal(self.color_of(coord), self.SPACE_COLOR):
                coord_not_found = False
        self.fill_gradient(coord, self.FOOD_COLOR)

    def fill_gradient(self, food_coord, intensity):
        """
        Fills all spaces in grid with gradient values

        food_coord - (x,y) coordinate of food
        intensity - float of starting intensity of food
        """

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                space = np.array([i,j])
                sqr_dist = (food_coord - space)**2
                grad = intensity/(np.sqrt(np.sum(sqr_dist))+1)**2
                self.draw(space, grad)

    def off_grid(self, coord):
        """
        Checks if argued coord is off of the grid

        coord - x,y integer coordinates as a tuple, list, or ndarray
        """

        return coord[0]<0 or coord[0]>=self.grid_size[0] or coord[1]<0 or coord[1]>=self.grid_size[1]

    def null_obs(self):
        """
        This function should be used to collect the observation for dead elegans.
        Returns [0,0] as nd array
        """
        return np.array([0,0], dtype=np.float32)

    def get_obs(self, elegan):
        """
        Returns an observation for the given elegan. The observation consists of the gradient
        to the left and right of the head.

        elegan - CElegan object
        """
        if elegan is None:
            return self.null_obs()
        obs = np.array([0,0], dtype=np.float32)
        left = elegan.step(elegan.head, (elegan.direction-1)%4)
        obs[0] = self.color_of(left)
        right = elegan.step(elegan.head, (elegan.direction+1)%4)
        obs[1] = self.color_of(right)
        return obs
