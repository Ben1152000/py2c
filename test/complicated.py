# This test contains features (i.e., strings and tuples) that are not yet
# implemented in py2c. It will *not* work.

def function1() -> None:
    pass

def function2(param1: int, param2: int) -> int:
    return (param1 + param2) * 2

def function3(param1: str) -> str:
    return param1[0]

def function4(param1: int) -> int:
    if (param1 == 0):
        return 0
    if (param1 == 1):
        return 1
    return function4(param1 - 1) + function4(param1 - 2)

def function5(param1: int) -> tuple[int, int]:
    const1: int = 3
    local1: int = function2(param1, 3)
    local2: int = local1 + const1
    local3: int = function4(local2)
    return (local3, local1)

def function6(param1: float) -> float:
    const1: int = 2
    return param1 / const1

const1: str = "2hello"
local1: str = function3(const1)
local2: int = int(local1)
local3: tuple[int, int] = function5(local2)
print(local3[0] + function5(3.14159))
