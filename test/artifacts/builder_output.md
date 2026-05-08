```python
from typing import List

def fibonacci(n: int) -> List[int]:
    """
    Calculate the first n numbers in the Fibonacci sequence.
    
    Args:
        n: The number of elements to generate.
        
    Returns:
        A list containing the first n Fibonacci numbers.
        
    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fibonacci.py <n>")
        sys.exit(1)
        
    try:
        n = int(sys.argv[1])
        print(fibonacci(n))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```