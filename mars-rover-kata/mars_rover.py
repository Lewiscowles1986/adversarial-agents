class MarsRover:
    """
    A Mars Rover that can move on a grid with wrapping and obstacle detection.

    Commands:
    - 'f': move forward
    - 'b': move backward
    - 'l': turn left
    - 'r': turn right
    """
    DIRECTIONS = ['N', 'E', 'S', 'W']
    MOVE_DELTAS = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }

    def __init__(self, x: int, y: int, direction: str, grid_size: tuple[int, int] = (100, 100), obstacles: list[tuple[int, int]] = None):
        """
        Initialize the rover with starting position, direction, grid size, and obstacles.
        """
        self._validate_inputs(x, y, direction, grid_size, obstacles)
        
        self.x = x
        self.y = y
        self.direction = direction
        self.grid_size = grid_size
        self.obstacles = set(obstacles or [])
        self.obstacle_encountered = False
        
        if (self.x, self.y) in self.obstacles:
            self.obstacle_encountered = True

    def _validate_inputs(self, x: int, y: int, direction: str, grid_size: tuple[int, int], obstacles: list[tuple[int, int]]):
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}. Must be one of {self.DIRECTIONS}")
        
        if grid_size[0] <= 0 or grid_size[1] <= 0:
            raise ValueError(f"Invalid grid size: {grid_size}. Dimensions must be positive.")

    def execute(self, commands: str) -> None:
        """
        Execute a sequence of commands.
        """
        if not isinstance(commands, str):
            return

        for command in commands:
            if command == 'l':
                self._turn_left()
            elif command == 'r':
                self._turn_right()
            elif command == 'f':
                self._move(forward=True)
            elif command == 'b':
                self._move(forward=False)
            
            if self.obstacle_encountered:
                break

    def get_status(self) -> str:
        """
        Return the current status of the rover in format "X:Y:D" or "O:X:Y:D" if an obstacle was hit.
        """
        prefix = "O:" if self.obstacle_encountered else ""
        return f"{prefix}{self.x}:{self.y}:{self.direction}"

    def _turn_left(self):
        """Turn the rover 90 degrees left."""
        idx = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(idx - 1) % 4]

    def _turn_right(self):
        """Turn the rover 90 degrees right."""
        idx = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(idx + 1) % 4]

    def _move(self, forward: bool):
        """Move the rover forward or backward, handling wrapping and obstacles."""
        if self.obstacle_encountered:
            return

        dx, dy = self.MOVE_DELTAS[self.direction]
        if not forward:
            dx, dy = -dx, -dy

        new_x = (self.x + dx) % self.grid_size[0]
        new_y = (self.y + dy) % self.grid_size[1]

        if (new_x, new_y) in self.obstacles:
            self.obstacle_encountered = True
        else:
            self.x = new_x
            self.y = new_y
