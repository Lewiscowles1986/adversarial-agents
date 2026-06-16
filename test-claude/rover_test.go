package main

import (
	"testing"
)

// ============================================================================
// UNIT TESTS
// ============================================================================

// TestRoverInitialization verifies rover can be created at valid positions
func TestRoverInitialization(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, err := NewRover(1, 2, North, grid)

	if err != nil {
		t.Fatalf("Failed to create rover: %v", err)
	}

	x, y := rover.GetPosition()
	if x != 1 || y != 2 {
		t.Errorf("Expected position (1, 2), got (%d, %d)", x, y)
	}
}

// TestRoverCannotStartAtInvalidPosition verifies rovers cannot be placed out of bounds
func TestRoverCannotStartAtInvalidPosition(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	_, err := NewRover(10, 10, North, grid)

	if err != ErrOutOfBounds {
		t.Errorf("Expected ErrOutOfBounds, got %v", err)
	}
}

// TestRoverCannotStartWithInvalidDirection verifies direction validation
func TestRoverCannotStartWithInvalidDirection(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	_, err := NewRover(1, 2, Direction(99), grid)

	if err != ErrInvalidDirection {
		t.Errorf("Expected ErrInvalidDirection, got %v", err)
	}
}

// TestStatusFormatting verifies Status() returns correct format
// CRITICAL: Tests single-digit AND multi-digit coordinates
func TestStatusFormatting(t *testing.T) {
	tests := []struct {
		x, y      int
		direction Direction
		expected  string
	}{
		{0, 0, North, "0 0 N"},
		{1, 2, East, "1 2 E"},
		{5, 8, South, "5 8 S"},
		{3, 4, West, "3 4 W"},
		{10, 5, North, "10 5 N"},       // Multi-digit X
		{5, 10, East, "5 10 E"},        // Multi-digit Y
		{10, 10, South, "10 10 S"},     // Both multi-digit
		{25, 75, West, "25 75 W"},      // Larger multi-digit
		{100, 200, North, "100 200 N"}, // Even larger
	}

	for _, test := range tests {
		grid, _ := NewGrid(200, 200)
		rover, _ := NewRover(test.x, test.y, test.direction, grid)
		status := rover.Status()

		if status != test.expected {
			t.Errorf("Expected '%s', got '%s'", test.expected, status)
		}
	}
}

// TestTurnLeft verifies left rotation from all directions
func TestTurnLeft(t *testing.T) {
	tests := []struct {
		from Direction
		to   Direction
	}{
		{North, West},
		{West, South},
		{South, East},
		{East, North},
	}

	for _, test := range tests {
		grid, _ := NewGrid(5, 5)
		rover, _ := NewRover(0, 0, test.from, grid)
		rover.TurnLeft()

		if rover.GetDirection() != test.to {
			t.Errorf("Turning left from %v: expected %v, got %v", test.from, test.to, rover.GetDirection())
		}
	}
}

// TestTurnRight verifies right rotation from all directions
func TestTurnRight(t *testing.T) {
	tests := []struct {
		from Direction
		to   Direction
	}{
		{North, East},
		{East, South},
		{South, West},
		{West, North},
	}

	for _, test := range tests {
		grid, _ := NewGrid(5, 5)
		rover, _ := NewRover(0, 0, test.from, grid)
		rover.TurnRight()

		if rover.GetDirection() != test.to {
			t.Errorf("Turning right from %v: expected %v, got %v", test.from, test.to, rover.GetDirection())
		}
	}
}

// TestMoveNorth verifies movement north increases Y
func TestMoveNorth(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, North, grid)
	rover.Move(grid)

	x, y := rover.GetPosition()
	if x != 0 || y != 1 {
		t.Errorf("Expected (0, 1), got (%d, %d)", x, y)
	}
}

// TestMoveEast verifies movement east increases X
func TestMoveEast(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, East, grid)
	rover.Move(grid)

	x, y := rover.GetPosition()
	if x != 1 || y != 0 {
		t.Errorf("Expected (1, 0), got (%d, %d)", x, y)
	}
}

// TestMoveSouth verifies movement south decreases Y
func TestMoveSouth(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 1, South, grid)
	rover.Move(grid)

	x, y := rover.GetPosition()
	if x != 0 || y != 0 {
		t.Errorf("Expected (0, 0), got (%d, %d)", x, y)
	}
}

// TestMoveWest verifies movement west decreases X
func TestMoveWest(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(1, 0, West, grid)
	rover.Move(grid)

	x, y := rover.GetPosition()
	if x != 0 || y != 0 {
		t.Errorf("Expected (0, 0), got (%d, %d)", x, y)
	}
}

// TestCannotMoveOutOfBounds verifies boundary enforcement
func TestCannotMoveOutOfBounds(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, West, grid)
	err := rover.Move(grid)

	if err != ErrOutOfBounds {
		t.Errorf("Expected ErrOutOfBounds, got %v", err)
	}

	// Verify position unchanged
	x, y := rover.GetPosition()
	if x != 0 || y != 0 {
		t.Errorf("Position should not change after failed move: got (%d, %d)", x, y)
	}
}

// TestCannotMoveIntoObstacle verifies obstacle detection
func TestCannotMoveIntoObstacle(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	grid.AddObstacle(0, 1)
	rover, _ := NewRover(0, 0, North, grid)
	err := rover.Move(grid)

	if err != ErrObstacleAtPosition {
		t.Errorf("Expected ErrObstacleAtPosition, got %v", err)
	}

	// Verify position unchanged
	x, y := rover.GetPosition()
	if x != 0 || y != 0 {
		t.Errorf("Position should not change after failed move: got (%d, %d)", x, y)
	}
}

// TestCannotMoveIntoAnotherRover verifies collision detection
func TestCannotMoveIntoAnotherRover(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover1, _ := NewRover(0, 0, North, grid)
	_, _ = NewRover(0, 1, South, grid) // rover2 blocks rover1's path

	err := rover1.Move(grid)
	if err != ErrRoverCollision {
		t.Errorf("Expected ErrRoverCollision, got %v", err)
	}

	// Verify position unchanged
	x, y := rover1.GetPosition()
	if x != 0 || y != 0 {
		t.Errorf("Position should not change after failed move: got (%d, %d)", x, y)
	}
}

// TestCommandSequenceLR verifies L and R commands
func TestCommandSequenceLR(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, North, grid)
	rover.ExecuteCommands("LMLMLMLMM", grid)

	if rover.Status() != "0 0 W" {
		t.Errorf("Expected '0 0 W', got '%s'", rover.Status())
	}
}

// TestComplexCommandSequence verifies multi-move commands
func TestComplexCommandSequence(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(1, 2, North, grid)
	rover.ExecuteCommands("LMLMLMLMM", grid)

	if rover.Status() != "1 3 N" {
		t.Errorf("Expected '1 3 N', got '%s'", rover.Status())
	}
}

// TestCommandSequenceWithWhitespace verifies whitespace tolerance
func TestCommandSequenceWithWhitespace(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(1, 1, North, grid)
	err := rover.ExecuteCommands("L M L M", grid)

	// L: Turn left (West), M: Move west to (0,1), L: Turn left (South), M: Move south to (0,0)
	if err != nil {
		t.Errorf("Command sequence should succeed, got %v", err)
	}

	if rover.Status() != "0 0 S" {
		t.Errorf("Expected '0 0 S', got '%s'", rover.Status())
	}
}

// TestEmptyCommandString verifies empty commands don't cause errors
func TestEmptyCommandString(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, North, grid)
	err := rover.ExecuteCommands("", grid)

	if err != nil {
		t.Errorf("Empty command string should not error, got %v", err)
	}

	if rover.Status() != "0 0 N" {
		t.Errorf("Position should not change: got '%s'", rover.Status())
	}
}

// TestInvalidCommand verifies error handling for bad commands
func TestInvalidCommand(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(0, 0, North, grid)
	err := rover.ExecuteCommands("LXM", grid)

	if err != ErrInvalidCommand {
		t.Errorf("Expected ErrInvalidCommand, got %v", err)
	}
}

// TestGridInitialization verifies grid creation
func TestGridInitialization(t *testing.T) {
	grid, err := NewGrid(5, 5)

	if err != nil {
		t.Fatalf("Failed to create grid: %v", err)
	}

	if grid.MaxX() != 5 || grid.MaxY() != 5 {
		t.Errorf("Expected (5, 5), got (%d, %d)", grid.MaxX(), grid.MaxY())
	}
}

// TestGridRejectsInvalidDimensions verifies validation
func TestGridRejectsInvalidDimensions(t *testing.T) {
	tests := []struct {
		maxX, maxY int
		shouldFail bool
	}{
		{5, 5, false},
		{0, 0, false},
		{-1, 5, true},
		{5, -1, true},
		{-5, -10, true},
	}

	for _, test := range tests {
		_, err := NewGrid(test.maxX, test.maxY)
		if test.shouldFail && err != ErrInvalidGridDimensions {
			t.Errorf("NewGrid(%d, %d) should fail with ErrInvalidGridDimensions, got %v", test.maxX, test.maxY, err)
		}
		if !test.shouldFail && err != nil {
			t.Errorf("NewGrid(%d, %d) should succeed, got %v", test.maxX, test.maxY, err)
		}
	}
}

// TestGridSynchronization verifies rover/grid position stays in sync
// CRITICAL: This validates the fix for the design flaw
func TestGridSynchronization(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover1, _ := NewRover(0, 0, North, grid)
	rover2, _ := NewRover(0, 2, South, grid)

	// Move rover1 and verify grid state matches
	rover1.Move(grid)
	if !grid.HasRover(0, 1) {
		t.Error("Grid should track rover1 at (0, 1)")
	}

	// Rover2 at (0, 2) tries to move south to (0, 1) where rover1 is
	err := rover2.Move(grid)
	if err != ErrRoverCollision {
		t.Errorf("Expected collision, got %v", err)
	}

	// Verify both rovers are still at correct positions in grid
	x1, y1, found1 := grid.GetRoverPosition(rover1)
	x2, y2, found2 := grid.GetRoverPosition(rover2)

	if !found1 || x1 != 0 || y1 != 1 {
		t.Errorf("Rover1 should be at (0, 1), grid shows (%d, %d)", x1, y1)
	}
	if !found2 || x2 != 0 || y2 != 2 {
		t.Errorf("Rover2 should be at (0, 2), grid shows (%d, %d)", x2, y2)
	}
}

// ============================================================================
// ACCEPTANCE TESTS (ATDD - Full scenario workflows)
// ============================================================================

// TestAcceptanceExample1 validates the classic example from problem statement
func TestAcceptanceExample1(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(1, 2, North, grid)
	rover.ExecuteCommands("LMLMLMLMM", grid)

	if rover.Status() != "1 3 N" {
		t.Errorf("Example 1 failed: expected '1 3 N', got '%s'", rover.Status())
	}
}

// TestAcceptanceExample2 validates second example from problem statement
func TestAcceptanceExample2(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover, _ := NewRover(3, 3, East, grid)
	rover.ExecuteCommands("MMRMMRMRRM", grid)

	if rover.Status() != "5 1 E" {
		t.Errorf("Example 2 failed: expected '5 1 E', got '%s'", rover.Status())
	}
}

// TestAcceptanceMultipleRoversWithCollisionAvoidance validates multi-rover scenario
func TestAcceptanceMultipleRoversWithCollisionAvoidance(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	rover1, _ := NewRover(1, 1, North, grid)
	rover2, _ := NewRover(1, 3, South, grid)

	// Move rover1 north
	rover1.ExecuteCommands("M", grid)
	if rover1.Status() != "1 2 N" {
		t.Errorf("Rover1 should be at '1 2 N', got '%s'", rover1.Status())
	}

	// Rover2 tries to move south from (1,3) to (1,2) where rover1 is - should fail
	err := rover2.Move(grid)
	if err != ErrRoverCollision {
		t.Errorf("Rover2 should detect collision, got %v", err)
	}

	// Rover2 should still be at original position
	if rover2.Status() != "1 3 S" {
		t.Errorf("Rover2 should be at '1 3 S', got '%s'", rover2.Status())
	}
}

// TestAcceptanceObstacleAvoidance validates obstacle scenario
func TestAcceptanceObstacleAvoidance(t *testing.T) {
	grid, _ := NewGrid(5, 5)
	grid.AddObstacle(0, 1)
	grid.AddObstacle(1, 1)

	rover, _ := NewRover(0, 0, North, grid)

	// Try to move north into obstacle - should fail
	err := rover.ExecuteCommands("M", grid)
	if err != ErrObstacleAtPosition {
		t.Errorf("Should detect obstacle, got %v", err)
	}

	// Rover should still be at start
	if rover.Status() != "0 0 N" {
		t.Errorf("Rover should be at '0 0 N', got '%s'", rover.Status())
	}

	// Rotate and move around obstacle (move east, then move north to (2,1))
	rover.ExecuteCommands("RMM", grid)
	if rover.Status() != "2 0 E" {
		t.Errorf("Rover should navigate around obstacle to '2 0 E', got '%s'", rover.Status())
	}
}

// TestAcceptanceLargeGrid validates operation on large coordinates
func TestAcceptanceLargeGrid(t *testing.T) {
	grid, _ := NewGrid(100, 100)
	rover, _ := NewRover(50, 50, North, grid)

	// Test that Status() correctly formats large coordinates
	status := rover.Status()
	if status != "50 50 N" {
		t.Errorf("Expected '50 50 N', got '%s'", status)
	}

	// Move and verify again
	rover.ExecuteCommands("MMMMMMMMMM", grid) // Move 10 north
	status = rover.Status()
	if status != "50 60 N" {
		t.Errorf("Expected '50 60 N', got '%s'", status)
	}
}

// TestAcceptanceBoundaryConditions validates grid edges
func TestAcceptanceBoundaryConditions(t *testing.T) {
	tests := []struct {
		maxX, maxY     int
		roverX, roverY int
		direction      Direction
		commands       string
		shouldSucceed  bool
		expectedStatus string
	}{
		// Moving to edge
		{5, 5, 5, 0, North, "MMMMM", true, "5 5 N"},
		// Attempting to go past edge
		{5, 5, 5, 5, North, "M", false, "5 5 N"},
		// All four corners
		{10, 10, 0, 0, South, "M", false, "0 0 S"},
		{10, 10, 0, 0, West, "M", false, "0 0 W"},
		{10, 10, 10, 10, North, "M", false, "10 10 N"},
		{10, 10, 10, 10, East, "M", false, "10 10 E"},
	}

	for _, test := range tests {
		grid, _ := NewGrid(test.maxX, test.maxY)
		rover, _ := NewRover(test.roverX, test.roverY, test.direction, grid)
		err := rover.ExecuteCommands(test.commands, grid)

		if test.shouldSucceed && err != nil {
			t.Errorf("Commands '%s' should succeed but got error: %v", test.commands, err)
		}
		if !test.shouldSucceed && err == nil {
			t.Errorf("Commands '%s' should fail but succeeded", test.commands)
		}
		if rover.Status() != test.expectedStatus {
			t.Errorf("Expected '%s', got '%s'", test.expectedStatus, rover.Status())
		}
	}
}

// TestAcceptanceComplexMultiRoverScenario validates realistic multi-rover scenario
func TestAcceptanceComplexMultiRoverScenario(t *testing.T) {
	grid, _ := NewGrid(8, 8)

	// Create three rovers
	rover1, _ := NewRover(1, 2, North, grid)
	rover2, _ := NewRover(3, 3, East, grid)
	rover3, _ := NewRover(5, 5, West, grid)

	// Execute their individual commands
	rover1.ExecuteCommands("LMLMLMLMM", grid)
	rover2.ExecuteCommands("MMRMMRMRRM", grid)
	rover3.ExecuteCommands("MMMRMMRM", grid)

	// Verify final positions
	tests := []struct {
		rover    *Rover
		expected string
	}{
		{rover1, "1 3 N"},
		{rover2, "5 1 E"},
		{rover3, "3 7 E"}, // Corrected: M(4,5)M(3,5)M(2,5)R(facing N)M(2,6)M(2,7)R(facing E)M(3,7)
	}

	for i, test := range tests {
		status := test.rover.Status()
		if status != test.expected {
			t.Errorf("Rover %d: expected '%s', got '%s'", i+1, test.expected, status)
		}
	}
}
