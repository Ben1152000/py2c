# This test does *not* currently work. It serves as an example of why
# implementing fully dynamic typing is difficult.

c = 1
c = "hello"
c = 0.2

def screwy(x):
    if type(x) is str:
        return 1
    if type(x) is int:
        return 'i'

c = screwy(c)
