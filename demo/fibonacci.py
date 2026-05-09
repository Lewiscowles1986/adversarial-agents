import argparse
from typing import Generator, List, Union

def generate_fibonacci(n: int) -> Generator[int, None, None]:
    """
    A generator that yields the first n numbers in the Fibonacci sequence.

    Time Complexity: O(n)
    Space Complexity: O(1) (excluding the yielded values)

    Args:
        n: The number of elements to generate.

    Yields:
        The next Fibonacci number in the sequence.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer.")
    if n < 0:
        raise ValueError("n must be a non-negative integer.")

    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b

def fibonacci(n: int) -> List[int]:
    """
    Calculate the first n numbers in the Fibonacci sequence and return them as a list.

    Time Complexity: O(n)
    Space Complexity: O(n) to store the result.

    Args:
        n: The number of elements to generate.

    Returns:
        A list containing the first n Fibonacci numbers.
    """
    return list(generate_fibonacci(n))

def main():
    parser = argparse.ArgumentParser(
        description="Calculate Fibonacci sequences."
    )
    parser.add_argument(
        "n", 
        type=int, 
        help="The number of elements to generate in the Fibonacci sequence."
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=10000,
        help="Safety limit for n (default: 10000) to prevent memory exhaustion."
    )
    
    args = parser.parse_args()
    
    if args.n > args.limit:
        print(f"Error: requested n ({args.n}) exceeds safety limit ({args.limit}).")
        return

    try:
        # Using the list-based version for simple CLI output
        print(fibonacci(args.n))
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
