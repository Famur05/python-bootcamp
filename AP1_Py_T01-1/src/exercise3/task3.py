def find_visited_places(figure):
    while len(figure) != 0:
        for x, y in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            new_coor_y = figure[0][0] + y
            new_coor_x = figure[0][1] + x
            if new_coor_y >= 0 and new_coor_y < matrix_len_size and new_coor_x >= 0 and new_coor_x < matrix_len_size:
                if matrix[new_coor_y][new_coor_x] == 1 and matrix_visited[new_coor_y][new_coor_x] == 0:
                    figure.append([new_coor_y, new_coor_x])
        element = figure.pop(0)
        matrix_visited[element[0]][element[1]] = 1 

with open("exercise3/input.txt", 'r') as file:
    matrix = [list(map(int, line.split())) for line in file]

matrix_len_size = len(matrix)

matrix_visited = [[0 for _ in range(matrix_len_size)] for _ in range(matrix_len_size)]

count_squares = 0
count_circles = 0

for i in range(matrix_len_size):
    for j in range(matrix_len_size):
        if matrix[i][j] == 1 and matrix_visited[i][j] != 1:
            count_x = 0
            count_y = 0
            coor_x_y = 1
            while count_x == count_y:
                if j + coor_x_y < matrix_len_size and matrix[i][j + coor_x_y] == 1:
                    count_x += 1
                if i + coor_x_y < matrix_len_size and matrix[i + coor_x_y][j] == 1:
                    count_y += 1
                else:
                    break
                coor_x_y += 1
            if count_x == count_y:
                count_squares += 1
            else:
                count_circles += 1
            
            figure = [[i, j]]
            find_visited_places(figure)  

print(count_squares, count_circles)