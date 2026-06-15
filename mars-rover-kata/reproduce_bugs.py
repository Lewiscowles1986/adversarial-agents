from mars_rover import MarsRover
import pytest

def test_invalid_direction():
    rover = MarsRover(0, 0, 'Z')
    try:
        rover.execute('l')
    except ValueError as e:
        print(f"Caught expected ValueError: {e}")

def test_none_commands():
    rover = MarsRover(0, 0, 'N')
    try:
        rover.execute(None)
    except TypeError as e:
        print(f"Caught expected TypeError: {e}")

if __name__ == "__main__":
    test_invalid_direction()
    test_none_commands()
