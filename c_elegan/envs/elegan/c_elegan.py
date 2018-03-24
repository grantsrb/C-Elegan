import numpy as np
from queue import deque

class CElegan():

    """
    The CElegan class holds all pertinent information regarding the CElegan's movement and body.
    The position of the c-elegan is tracked using a queue that stores the positions of the body.

    Note:
    A potentially more space efficient implementation could track directional changes rather
    than tracking each location of the c-elegan's body.
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, head_coord_start):
        """
        head_coord_start - tuple, list, or ndarray denoting the starting coordinates for the c-elegan's head
        """
        self.direction = self.SOUTH
        self.head = np.asarray(head_coord_start).astype(np.int)
        self.head_color = -1
        self.body = deque()
        body_length = 3
        for i in range(body_length-1, 0, -1):
            self.body.append(self.head-np.asarray([0,i]).astype(np.int))

    def step(self, coord, direction):
        """
        Finds the coordinate corresponding to a step in the specified direction 
        from the specified coordinate.

        coord - list, tuple, or numpy array
        direction - integer from 0-3 inclusive.
            0: NORTH
            1: EAST
            2: SOUTH
            3: WEST
        """

        assert direction < 4 and direction >= 0

        if direction == self.NORTH:
            return np.asarray([coord[0], coord[1]-1]).astype(np.int)
        elif direction == self.EAST:
            return np.asarray([coord[0]+1, coord[1]]).astype(np.int)
        elif direction == self.SOUTH:
            return np.asarray([coord[0], coord[1]+1]).astype(np.int)
        else:
            return np.asarray([coord[0]-1, coord[1]]).astype(np.int)

    def action(self, direction):
        """
        This method sets a new head coordinate and appends the old head
        into the body queue. The Controller class handles popping the
        last piece of the body if no food is eaten on this step.

        The direction can be any integer value, but will be collapsed
        to 0, 1, or 2 corresponding to left, straight, and right respectively.

        direction - integer from 0-2 inclusive.
            0: left
            1: straight
            2: right
        """

        # Ensure literal direction is either 0, 1, 2, or 3
        direction = (int(direction) % 3)-1
        self.direction = (self.direction + direction) % 4

        self.body.append(self.head)
        self.body.popleft()
        self.head = self.step(self.head, self.direction)

        return self.head
