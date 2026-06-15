import pytest
from mars_rover import MarsRover

class TestMarsRoverAcceptance:
    """
    Acceptance tests for the Mars Rover kata.
    These tests follow a BDD-style Given/When/Then structure.
    """

    def test_basic_movement_and_turning(self):
        """
        Scenario: Move and turn in the open field
            Given a rover is at position (0, 0) facing North
            When it receives commands "ffrff"
            Then its final position should be (2, 2) facing East
        """
        rover = MarsRover(x=0, y=0, direction='N')
        rover.execute("ffrff")
        assert rover.get_status() == "2:2:E"

    def test_grid_wrapping(self):
        """
        Scenario: Wrapping around the grid edges
            Given a rover is at position (0, 0) facing North on a 10x10 grid
            When it moves forward 10 times
            Then it should wrap back to (0, 0) facing North
        """
        rover = MarsRover(x=0, y=0, direction='N', grid_size=(10, 10))
        rover.execute("ffffffffff")
        assert rover.get_status() == "0:0:N"

    def test_obstacle_detection(self):
        """
        Scenario: Encountering an obstacle
            Given a rover is at position (0, 0) facing North
            And there is an obstacle at (0, 2)
            When it receives commands "fff"
            Then it should stop at (0, 1) facing North
            And it should report an obstacle encountered at (0, 2)
        """
        rover = MarsRover(x=0, y=0, direction='N', obstacles=[(0, 2)])
        rover.execute("fff")
        assert rover.get_status() == "O:0:1:N"

    def test_backward_movement_and_wrapping(self):
        """
        Scenario: Moving backward with wrapping
            Given a rover is at position (0, 0) facing North on a 100x100 grid
            When it moves backward once
            Then its position should be (0, 99) facing North
        """
        rover = MarsRover(x=0, y=0, direction='N', grid_size=(100, 100))
        rover.execute("b")
        assert rover.get_status() == "0:99:N"

    def test_starting_on_obstacle_immediately_reports_collision(self):
        """
        Scenario: Rover deployed on an obstacle
            Given a rover is deployed at (1, 1) facing East
            And there is an obstacle at (1, 1)
            Then it should immediately report an obstacle
            And it should not move when commands are issued
        """
        rover = MarsRover(x=1, y=1, direction='E', obstacles=[(1, 1)])
        assert rover.get_status() == "O:1:1:E"
        rover.execute("f")
        assert rover.get_status() == "O:1:1:E"
