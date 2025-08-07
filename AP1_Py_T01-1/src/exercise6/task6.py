import json

try:
    with open('exercise6/input.txt', 'r') as file:
        json_data = json.load(file)
    if not isinstance(json_data, dict) or 'list1' not in json_data or 'list2' not in json_data:
        raise ValueError
    for key in ['list1', 'list2']:
        if not isinstance(json_data[key], list):
            raise ValueError
        for item in json_data[key]:
            if not isinstance(item, dict):
                raise ValueError
            
except ValueError:
    print('Invalid input format')
else:
    list0 = json_data['list1'] + json_data['list2']
    sorted_list = sorted(list0, key=lambda d: d['year'])
    output_json = {"list0": sorted_list}
    json_output = json.dumps(output_json, indent=2)
    print(json_output)
    