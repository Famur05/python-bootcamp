def get_finally_prices_list(cars_info, all_work_time):
    cars_by_year = dict()
    for issue_year, price, work_time in cars_info:
        if issue_year not in cars_by_year:
            cars_by_year[issue_year] = [[price, work_time]]
        else:
            cars_by_year[issue_year] += [[price, work_time]]

    finally_prices_list = []
    for key in cars_by_year.keys():
        if len(cars_by_year[key]) >= 2:
            for i in range(len(cars_by_year[key])):
                for j in range(i + 1, len(cars_by_year[key])):
                    if cars_by_year[key][i][1] + cars_by_year[key][j][1] == all_work_time:
                        finally_prices_list.append(cars_by_year[key][i][0] + cars_by_year[key][j][0])
    return finally_prices_list         

try:
    cars_number, all_work_time = map(int, input().split())
    cars_info = [list(map(int, input().split())) for _ in range(cars_number)]
    if cars_number <= 0 or all_work_time <= 0:
        raise ValueError
    for i in range(cars_number):
        if len(cars_info[i]) > 3:
            raise ValueError
        else:
            for j in range(3):
                if cars_info[i][j] <= 0:
                    raise ValueError

    finally_prices_list = get_finally_prices_list(cars_info, all_work_time)

    if not finally_prices_list:
        raise ValueError
    
    print(min(finally_prices_list))

except ValueError:
    print('Invalid input format')