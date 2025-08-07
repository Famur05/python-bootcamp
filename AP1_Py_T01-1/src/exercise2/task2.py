number = int(input())
arr = []
flag = True

if number < 0:
    flag = False
else:
    while number > 0:
        arr.append(number % 10)
        number //= 10

    flag = arr == arr[::-1]

print(flag)