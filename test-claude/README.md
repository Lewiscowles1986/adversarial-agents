# Mars Rover ATDD Implementation (Fixed)

A complete, production-ready Mars Rover kata implementation in Go using Acceptance Test-Driven Development (ATDD).

## Key Fixes from Original Implementation

This version corrects **three critical issues** found in the original:

### 1. ✅ Status() ASCII Bug Fixed
**Problem:** Original used `string(rune(x+48))` which only works for single-digit coordinates.
- Position (10, 5) → incorrectly output `: 5 N` instead of `10 5 N`
- All tests used 0-8 coordinates, hiding the bug

**Solution:** Uses `fmt.Sprintf("%d %d %s", x, y, direction)` for correct formatting at any coordinate.

### 2. ✅ Grid/Rover Synchronization Fixed
**Problem:** Rover's internal position and Grid's rover map could drift out of sync.
- `Move()` updated rover coordinates but didn't update `grid.rovers`
- Required manual `UpdateRoverPosition()` calls, which is fragile
- Collision detection could fail with stale position data

**Solution:** `Move()` now automatically updates grid state. Internal consistency guaranteed.

### 3. ✅ Input Validation Added
**Problem:** Grid accepted invalid dimensions (negative, zero).

**Solution:** 
- `NewGrid()` returns error for invalid dimensions
- `UpdateRoverPosition()` validates coordinates before accepting
- Comprehensive error handling throughout

## Features

✅ **Rover Commands**: L (turn left), R (turn right), M (move)  
✅ **Position Tracking**: X, Y coordinates on configurable grid  
✅ **Direction Tracking**: N, S, E, W compass directions  
✅ **Grid Management**: Configurable dimensions with validation  
✅ **Obstacle Detection**: Prevents movement into obstacles  
✅ **Command Sequences**: Process multiple commands via STDIN  
✅ **Error Handling**: 9 error types, no panics  
✅ **Multi-Rover Support**: Multiple rovers with collision avoidance  
✅ **Boundary Enforcement**: Grid edge detection and enforcement  

## Test Coverage

**27 Acceptance Tests** covering:
- Initialization and validation
- All rotations (L/R from all 4 directions)
- Movement in all 4 cardinal directions
- Boundary conditions (all grid edges)
- Obstacle detection and prevention
- Rover collision avoidance
- Command sequences (single and complex)
- Multi-digit coordinates (tests the ASCII bug fix)
- Grid dimension validation
- Error conditions and recovery
- Whitespace tolerance

## Build & Run

```bash
# Build
go build -o mars-rover

# Run tests (27 tests, all passing)
go test -v

# Interactive mode (STDIN input)
./mars-rover

# Batch mode
./mars-rover < input.txt
```

## Input Format

```
maxX maxY                 # Grid dimensions
x y DIRECTION            # Rover 1 position & direction
COMMANDS                 # Rover 1 command sequence
x y DIRECTION            # Rover 2 position & direction
COMMANDS                 # Rover 2 command sequence
...
```

## Example

Input:
```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Output:
```
1 3 N
5 1 E
```

## API Reference

### Rover
- `NewRover(x, y int, direction Direction, grid *Grid) (*Rover, error)`
- `Status() string` - Returns "x y DIRECTION"
- `Move(grid *Grid) error` - Move one step forward
- `TurnLeft()` - Rotate 90° counterclockwise
- `TurnRight()` - Rotate 90° clockwise
- `ExecuteCommands(commands string, grid *Grid) error`

### Grid
- `NewGrid(maxX, maxY int) (*Grid, error)` - Create grid with validation
- `AddObstacle(x, y int) error`
- `HasObstacle(x, y int) bool`
- `HasRover(x, y int) bool`
- `IsValid(x, y int) bool`
- `RegisterRover(r *Rover, x, y int) error`

### Errors
```go
ErrRoverAlreadyExists
ErrRoverNotFound
ErrObstacleAtPosition
ErrOutOfBounds
ErrInvalidCommand
ErrInvalidDirection
ErrInvalidCoordinates
ErrInvalidGridDimensions
ErrRoverCollision
```

## Design Principles

1. **ATDD**: Tests verify behavior through full scenarios, not just unit test specifics
2. **Type Safety**: Direction is enum, not string
3. **Error Handling**: Explicit error returns, no panics
4. **Immutability**: Grid dimensions cannot change after creation
5. **Synchronization**: Automatic grid state updates prevent drift
6. **Validation**: All inputs validated at boundaries

## Architecture

- **rover.go** (150 lines): Core rover logic with synchronized grid updates
- **grid.go** (100 lines): Grid management with input validation
- **errors.go** (15 lines): 9 custom error types
- **main.go** (100 lines): CLI with comprehensive error handling
- **rover_test.go** (520 lines): 27 comprehensive acceptance tests
