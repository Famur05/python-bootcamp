def convert_str_int(input_line):
    convert_number = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9 
    }
    arr_line = input_line.split('.')
    integer_part_str = arr_line[0]
    fractional_part_str = arr_line[1]
    is_have_minus = False
    if integer_part_str[0] == '-':
        integer_part_str = integer_part_str.lstrip('-')
        is_have_minus = True
    integer_part_num = 0
    fractional_part_num = 0
    for num in integer_part_str:
        integer_part_num = integer_part_num * 10 + convert_number[num] 
    for num in fractional_part_str:
        fractional_part_num = fractional_part_num * 10 + convert_number[num]
    fractional_part_num /= 10 ** len(fractional_part_str)

    finally_float = (integer_part_num + fractional_part_num) * 2
    if is_have_minus:
        finally_float *= -1
    return finally_float

try:
    input_line = input()
    if input_line.count('.') != 1 or not (input_line[0] == '-' and input_line[1:].replace('.', '').isdigit()
    or input_line.replace('.', '').isdigit()):
        raise ValueError
except ValueError:
    print('Invalid input format')
else:
    finally_float = convert_str_int(input_line)
    print(format(finally_float, '.3f'))