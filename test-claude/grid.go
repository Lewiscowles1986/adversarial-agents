package main

// Grid represents a flat rectangular grid with obstacle tracking
type Grid struct {
	maxX      int
	maxY      int
	obstacles map[[2]int]bool
	rovers    map[*Rover][2]int
}

// NewGrid creates a new grid with specified dimensions
// Returns error if dimensions are invalid (negative or zero)
func NewGrid(maxX, maxY int) (*Grid, error) {
	if maxX < 0 || maxY < 0 {
		return nil, ErrInvalidGridDimensions
	}
	return &Grid{
		maxX:      maxX,
		maxY:      maxY,
		obstacles: make(map[[2]int]bool),
		rovers:    make(map[*Rover][2]int),
	}, nil
}

// AddObstacle adds an obstacle at position (x, y)
func (g *Grid) AddObstacle(x, y int) error {
	if !g.IsValid(x, y) {
		return ErrOutOfBounds
	}
	g.obstacles[[2]int{x, y}] = true
	return nil
}

// IsValid checks if coordinates are within grid bounds
func (g *Grid) IsValid(x, y int) bool {
	return x >= 0 && x <= g.maxX && y >= 0 && y <= g.maxY
}

// HasObstacle checks if there's an obstacle at (x, y)
func (g *Grid) HasObstacle(x, y int) bool {
	return g.obstacles[[2]int{x, y}]
}

// HasRover checks if another rover exists at (x, y)
func (g *Grid) HasRover(x, y int) bool {
	for _, pos := range g.rovers {
		if pos[0] == x && pos[1] == y {
			return true
		}
	}
	return false
}

// RegisterRover adds rover to grid at initial position
func (g *Grid) RegisterRover(r *Rover, x, y int) error {
	if !g.IsValid(x, y) {
		return ErrOutOfBounds
	}
	if g.HasRover(x, y) {
		return ErrRoverCollision
	}
	g.rovers[r] = [2]int{x, y}
	return nil
}

// UpdateRoverPosition updates rover's position in grid
// Internal method - assumes Move() has already validated the position
// NOTE: This is called automatically by Rover.Move(), not manually
func (g *Grid) UpdateRoverPosition(r *Rover, x, y int) error {
	// Validate before accepting position
	if !g.IsValid(x, y) {
		return ErrOutOfBounds
	}

	// Check for other rovers at destination
	for existingRover, pos := range g.rovers {
		if existingRover != r && pos[0] == x && pos[1] == y {
			return ErrRoverCollision
		}
	}

	g.rovers[r] = [2]int{x, y}
	return nil
}

// GetRoverPosition returns the current position of a rover
func (g *Grid) GetRoverPosition(r *Rover) (x, y int, found bool) {
	pos, found := g.rovers[r]
	if found {
		return pos[0], pos[1], true
	}
	return 0, 0, false
}

// MaxX returns the grid's maximum X coordinate
func (g *Grid) MaxX() int {
	return g.maxX
}

// MaxY returns the grid's maximum Y coordinate
func (g *Grid) MaxY() int {
	return g.maxY
}

// ClearObstacles removes all obstacles from the grid
func (g *Grid) ClearObstacles() {
	g.obstacles = make(map[[2]int]bool)
}

// RemoveRover removes a rover from the grid
func (g *Grid) RemoveRover(r *Rover) {
	delete(g.rovers, r)
}

// RoverCount returns the number of rovers on the grid
func (g *Grid) RoverCount() int {
	return len(g.rovers)
}
