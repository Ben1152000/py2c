def f() -> float:
    a = int
    b = float
    c = ('n', 'return')
    def g(a: int, b: int, c: float, d: int, e: float, f: float) -> float:
        return 3.14159 * a
    return g(2, 0, 0, 0, 0, 0)
f()