vector_1_coor = input()
vector_2_coor = input()

vector_1_coor = vector_1_coor.split(' ')
vector_2_coor = vector_2_coor.split(' ')

sum = 0
for i in range(len(vector_1_coor)):
    sum += float(vector_1_coor[i]) * float(vector_2_coor[i])

print(sum)