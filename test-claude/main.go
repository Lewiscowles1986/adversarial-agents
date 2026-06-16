package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	// Read grid dimensions
	if !scanner.Scan() {
		fmt.Fprintf(os.Stderr, "ERROR: No input provided\n")
		os.Exit(1)
	}

	gridInput := strings.Fields(scanner.Text())
	if len(gridInput) != 2 {
		fmt.Fprintf(os.Stderr, "ERROR: Grid dimensions must be 'maxX maxY'\n")
		os.Exit(1)
	}

	maxX, err := strconv.Atoi(gridInput[0])
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Invalid maxX: %v\n", err)
		os.Exit(1)
	}

	maxY, err := strconv.Atoi(gridInput[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Invalid maxY: %v\n", err)
		os.Exit(1)
	}

	// Create grid with validation
	grid, err := NewGrid(maxX, maxY)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: %v\n", err)
		os.Exit(1)
	}

	roverNum := 0
	for scanner.Scan() {
		roverNum++

		// Read rover position and direction
		posLine := strings.Fields(scanner.Text())
		if len(posLine) != 3 {
			fmt.Fprintf(os.Stderr, "ERROR: Rover %d position format must be 'x y DIRECTION'\n", roverNum)
			os.Exit(1)
		}

		x, err := strconv.Atoi(posLine[0])
		if err != nil {
			fmt.Fprintf(os.Stderr, "ERROR: Invalid x coordinate for rover %d: %v\n", roverNum, err)
			os.Exit(1)
		}

		y, err := strconv.Atoi(posLine[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "ERROR: Invalid y coordinate for rover %d: %v\n", roverNum, err)
			os.Exit(1)
		}

		// Parse direction
		dirStr := strings.ToUpper(posLine[2])
		var direction Direction
		switch dirStr {
		case "N":
			direction = North
		case "E":
			direction = East
		case "S":
			direction = South
		case "W":
			direction = West
		default:
			fmt.Fprintf(os.Stderr, "ERROR: Invalid direction '%s' for rover %d\n", dirStr, roverNum)
			os.Exit(1)
		}

		// Create rover
		rover, err := NewRover(x, y, direction, grid)
		if err != nil {
			fmt.Fprintf(os.Stderr, "ERROR: Cannot create rover %d at (%d, %d): %v\n", roverNum, x, y, err)
			os.Exit(1)
		}

		// Read command sequence
		if !scanner.Scan() {
			fmt.Fprintf(os.Stderr, "ERROR: Expected command sequence for rover %d\n", roverNum)
			os.Exit(1)
		}

		commands := scanner.Text()

		// Execute commands
		if err := rover.ExecuteCommands(commands, grid); err != nil {
			fmt.Fprintf(os.Stderr, "ERROR: Rover %d execution failed: %v\n", roverNum, err)
			os.Exit(1)
		}

		// Output final position
		fmt.Println(rover.Status())
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Failed to read input: %v\n", err)
		os.Exit(1)
	}
}
