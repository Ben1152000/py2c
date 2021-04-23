def f_i(n):
    a = [0, 1]
    for i in range(2, n+1):
        a.append(a[i-1] + a[i-2])
    return a[n]

def f_r(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return f_r(n-1) + f_r(n-2)

print("Fibonacci Numbers:")
for i in range(10):
    print(f_i(i), f_r(i))