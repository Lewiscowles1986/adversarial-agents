import unittest
from fibonacci import fibonacci, generate_fibonacci

class TestFibonacci(unittest.TestCase):
    def test_fibonacci_list(self):
        self.assertEqual(fibonacci(0), [])
        self.assertEqual(fibonacci(1), [0])
        self.assertEqual(fibonacci(2), [0, 1])
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_fibonacci_generator(self):
        gen = generate_fibonacci(5)
        self.assertEqual(next(gen), 0)
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 2)
        self.assertEqual(next(gen), 3)
        with self.assertRaises(StopIteration):
            next(gen)

    def test_fibonacci_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_fibonacci_invalid_type(self):
        with self.assertRaises(TypeError):
            fibonacci("5") # type: ignore
        with self.assertRaises(TypeError):
            fibonacci(5.5) # type: ignore

if __name__ == "__main__":
    unittest.main()
