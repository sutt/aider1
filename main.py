from typing import Callable

def hello() -> None:
    print("hello world")

def factorial(n: int) -> int:
    if n == 0:
        return 1
    return n * factorial(n-1)

def get_factorial() -> Callable[[int], int]:
    return factorial

if __name__ == "__main__":
    hello()
    result = factorial(5)
    print(f"Factorial of 5 is: {result}")
