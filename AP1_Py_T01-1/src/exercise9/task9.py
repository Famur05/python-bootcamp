N, x0 = input().split()
N = int(N)
x0 = float(x0)

coefficients = []
for _ in range(N + 1):
    line = input()
    coefficients.insert(0, float(line))  

derivative = 0
for degree, coefficient in enumerate(coefficients[1:], start=1):
    derivative += degree * coefficient * (x0 ** (degree - 1))

print(f"{derivative:.3f}")
