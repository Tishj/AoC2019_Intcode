import json

area = dict()
with open("map.json") as f:
	raw = json.load(f)
	for key, value in raw.items():
		x,y = [int(x) for x in key.strip('(').strip(')').split(', ')]
		area[(x,y)] = value

y_values = [key[1] for key in area.keys()]
x_values = [key[0] for key in area.keys()]

min_x = min(x_values)
min_y = min(y_values)
max_x = max(x_values)
max_y = max(y_values)

space = [[' ' for _ in range(-min_x + max_x + 1)] for _ in range(-min_y + max_y + 1)]

for key, value in area.items():
	x,y = key
	x += -min_x
	y += -min_y
	visual = ' '
	if key == (0,0):
		visual = 'S'
	elif value == 1:
		visual = '.'
	elif value == 2:
		visual = '#'
	else:
		visual = 'X'
	space[y][x] = visual

output = ""
for line in space:
	output += " ".join(line)
	output += "\n"

print(output)