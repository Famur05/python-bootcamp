def pascals_triangle(n):
    triangle = []
    for i in range(n):
        line = [1]  
        if triangle:  
            last_line = triangle[-1]
            line.extend([last_line[j] + last_line[j + 1] for j in range(len(last_line) - 1)])
            line.append(1)  
        triangle.append(line)
    return triangle

try:
    n = int(input())
    if n <= 0:
        raise ValueError
except ValueError:
    print("Natural number was expected")
else:
    triangle = pascals_triangle(n)
    for line in triangle:
        print(" ".join(map(str, line)))
