n, m = map(int, input().split())
field = [list(map(int, input().split())) for _ in range(n)]
field_solution = [[0 for _ in range(m)] for _ in range(n)]
field_solution[0][0] = field[0][0]
for i in range(1, n):
    field_solution[i][0] = field_solution[i - 1][0] + field[i][0]
for i in range(1, m):
    field_solution[0][i] = field_solution[0][i - 1] + field[0][i]
for i in range(1, n):
    for j in range(1, m):
        next_step = field_solution[i][j - 1] if field_solution[i][j - 1] > field_solution[i - 1][j] else field_solution[i - 1][j]
        field_solution[i][j] = field[i][j] + next_step
print(field_solution[n - 1][m - 1])
