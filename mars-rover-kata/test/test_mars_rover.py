import pytest
from mars_rover import MarsRover

def test_initial_position():
    rover = MarsRover(1, 2, 'E')
    assert rover.get_status() == "1:2:E"

@pytest.mark.parametrize("command,expected", [
    ("f", "0:1:N"),
    ("b", "0:99:N"),
    ("l", "0:0:W"),
    ("r", "0:0:E"),
])
def test_single_commands(command, expected):
    rover = MarsRover(0, 0, 'N')
    rover.execute(command)
    assert rover.get_status() == expected

def test_wrapping_east():
    rover = MarsRover(99, 0, 'E', grid_size=(100, 100))
    rover.execute("f")
    assert rover.get_status() == "0:0:E"

def test_wrapping_west():
    rover = MarsRover(0, 0, 'W', grid_size=(100, 100))
    rover.execute("f")
    assert rover.get_status() == "99:0:W"

def test_wrapping_south():
    rover = MarsRover(0, 0, 'S', grid_size=(100, 100))
    rover.execute("f")
    assert rover.get_status() == "0:99:S"

def test_obstacle_detection_stops_movement():
    rover = MarsRover(0, 0, 'N', obstacles=[(0, 2)])
    rover.execute("fff")
    assert rover.get_status() == "O:0:1:N"

def test_complex_movement():
    rover = MarsRover(0, 0, 'N')
    rover.execute("ffrff")
    assert rover.get_status() == "2:2:E"
    rover.execute("llf")
    assert rover.get_status() == "1:2:W"

# Edge Case Tests based on Critic Review

def test_invalid_direction_raises_error():
    with pytest.raises(ValueError, match="Invalid direction"):
        MarsRover(0, 0, 'Z')

def test_starting_on_obstacle():
    rover = MarsRover(0, 0, 'N', obstacles=[(0, 0)])
    assert rover.get_status() == "O:0:0:N"
    rover.execute("f")
    assert rover.get_status() == "O:0:0:N"  # Should not move if already hit an obstacle

def test_none_input_handled_gracefully():
    rover = MarsRover(0, 0, 'N')
    rover.execute(None)
    assert rover.get_status() == "0:0:N"

def test_invalid_grid_size_raises_error():
    with pytest.raises(ValueError, match="Invalid grid size"):
        MarsRover(0, 0, 'N', grid_size=(0, 100))
    with pytest.raises(ValueError, match="Invalid grid size"):
        MarsRover(0, 0, 'N', grid_size=(100, -1))

def test_invalid_commands_ignored():
    rover = MarsRover(0, 0, 'N')
    rover.execute("fxr") # 'x' is invalid, should be ignored or at least not crash
    assert rover.get_status() == "0:1:E"
