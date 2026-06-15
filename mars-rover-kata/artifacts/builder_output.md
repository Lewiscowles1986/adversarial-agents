The Mars Rover code kata has been completed using ATDD. 

### Implementation: `mars_rover.py`
```python
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

    def __init__(self, x: int, y: int, direction: str, grid_size: tuple[int, int] = (100, 100), obstacles: list[tuple[int, int]] = None):
        """
        Initialize the rover with starting position, direction, grid size, and obstacles.
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.grid_size = grid_size
        self.obstacles = obstacles or []
        self.obstacle_encountered = False

    def execute(self, commands: str) -> None:
        """
        Execute a sequence of commands.
        """
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
        dx, dy = 0, 0
        if self.direction == 'N':
            dy = 1 if forward else -1
        elif self.direction == 'E':
            dx = 1 if forward else -1
        elif self.direction == 'S':
            dy = -1 if forward else 1
        elif self.direction == 'W':
            dx = -1 if forward else 1

        new_x = (self.x + dx) % self.grid_size[0]
        new_y = (self.y + dy) % self.grid_size[1]

        if (new_x, new_y) in self.obstacles:
            self.obstacle_encountered = True
        else:
            self.x = new_x
            self.y = new_y
```

### Verification
A total of 13 tests (acceptance and unit) were implemented and are passing:
- **Acceptance Tests:** `test/test_mars_rover_acceptance.py`
- **Unit Tests:** `test/test_mars_rover.py`

Run tests using:
```bash
pytest test/test_mars_rover.py test/test_mars_rover_acceptance.py
```