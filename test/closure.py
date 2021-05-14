def f() -> float:
    def g(n: int) -> float:
        return 3.14159 * n
    return g(2)
f()