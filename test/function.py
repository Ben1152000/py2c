def g(x: int) -> int:
    return x + 1

def f() -> float:
    b: int = g(1)
    b = g(b)
    return 3.14159

a: float = f()
print(a)
