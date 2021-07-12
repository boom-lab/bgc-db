import json
f = open('test.json')
data = json.load(f)

print(len(data['1902303']['dis_x']))