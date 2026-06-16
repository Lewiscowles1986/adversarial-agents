package main

import "errors"

var (
	ErrRoverAlreadyExists    = errors.New("rover already exists at that position")
	ErrRoverNotFound         = errors.New("rover not found")
	ErrObstacleAtPosition    = errors.New("obstacle detected at next position")
	ErrOutOfBounds           = errors.New("destination out of grid bounds")
	ErrInvalidCommand        = errors.New("invalid command")
	ErrInvalidDirection      = errors.New("invalid direction")
	ErrInvalidCoordinates    = errors.New("invalid coordinates")
	ErrInvalidGridDimensions = errors.New("grid dimensions must be non-negative")
	ErrRoverCollision        = errors.New("another rover exists at that position")
)
