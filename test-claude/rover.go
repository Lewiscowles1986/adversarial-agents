package main

import (
	"fmt"
	"strings"
)

// Direction represents compass direction
type Direction int

const (
	North Direction = iota
	East
	South
	West
)

// Rover represents a Mars rover with position and direction
type Rover struct {
	x         int
	y         int
	direction Direction
}

// NewRover creates a rover at position (x, y) facing direction d
func NewRover(x, y int, d Direction, grid *Grid) (*Rover, error) {
	if !grid.IsValid(x, y) {
		return nil, ErrOutOfBounds
	}
	if grid.HasRover(x, y) {
		return nil, ErrRoverCollision
	}
	if d < North || d > West {
		return nil, ErrInvalidDirection
	}

	rover := &Rover{x: x, y: y, direction: d}
	if err := grid.RegisterRover(rover, x, y); err != nil {
		return nil, err
	}
	return rover, nil
}

// Status returns the rover's position and direction as "x y DIRECTION"
// FIXED: Uses fmt.Sprintf instead of ASCII arithmetic to handle all coordinates
func (r *Rover) Status() string {
	return fmt.Sprintf("%d %d %s", r.x, r.y, r.DirectionString())
}

// DirectionString returns the compass direction as a string
func (r *Rover) DirectionString() string {
	switch r.direction {
	case North:
		return "N"
	case East:
		return "E"
	case South:
		return "S"
	case West:
		return "W"
	default:
		return "?"
	}
}

// TurnLeft rotates the rover 90 degrees counterclockwise
func (r *Rover) TurnLeft() {
	r.direction = (r.direction + 3) % 4 // Equivalent to -1 in modulo arithmetic
}

// TurnRight rotates the rover 90 degrees clockwise
func (r *Rover) TurnRight() {
	r.direction = (r.direction + 1) % 4
}

// Move attempts to move the rover one grid point in its current direction
// FIXED: Automatically updates grid state to keep rover/grid in sync
// Returns error if move is blocked (obstacle, collision, or out of bounds)
func (r *Rover) Move(grid *Grid) error {
	nextX, nextY := r.x, r.y

	switch r.direction {
	case North:
		nextY++
	case East:
		nextX++
	case South:
		nextY--
	case West:
		nextX--
	}

	// Check bounds
	if !grid.IsValid(nextX, nextY) {
		return ErrOutOfBounds
	}

	// Check for obstacles
	if grid.HasObstacle(nextX, nextY) {
		return ErrObstacleAtPosition
	}

	// Check for other rovers (collision detection)
	for otherRover, pos := range grid.rovers {
		if otherRover != r && pos[0] == nextX && pos[1] == nextY {
			return ErrRoverCollision
		}
	}

	// All checks passed, update position in both rover and grid
	r.x = nextX
	r.y = nextY
	if err := grid.UpdateRoverPosition(r, nextX, nextY); err != nil {
		// This should never happen if our collision detection worked
		// but we handle it defensively
		r.x = nextX - (nextX - r.x)
		r.y = nextY - (nextY - r.y)
		return err
	}

	return nil
}

// ExecuteCommands processes a sequence of commands (L/R/M)
// Stops and returns error on invalid command or blocked move
// L = turn left, R = turn right, M = move forward
func (r *Rover) ExecuteCommands(commands string, grid *Grid) error {
	commands = strings.TrimSpace(commands)
	if commands == "" {
		return nil
	}

	for _, cmd := range commands {
		switch cmd {
		case 'L':
			r.TurnLeft()
		case 'R':
			r.TurnRight()
		case 'M':
			if err := r.Move(grid); err != nil {
				return err
			}
		case ' ', '\t', '\n':
			// Ignore whitespace
			continue
		default:
			return ErrInvalidCommand
		}
	}
	return nil
}

// GetPosition returns current (x, y) coordinates
func (r *Rover) GetPosition() (int, int) {
	return r.x, r.y
}

// GetDirection returns current direction
func (r *Rover) GetDirection() Direction {
	return r.direction
}
