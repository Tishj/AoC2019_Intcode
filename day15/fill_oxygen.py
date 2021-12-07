import time

area = list()
for line in open("map_real").read().split("\n"):
	area.append([x[0] for x in [line[i:i+2] for i in range(0, len(line), 2)]])

def get_start_position(area):
	for y, line in enumerate(area):
		for x, char in enumerate(line):
			if area[y][x] == 'S':
				return (x,y)

def visualize(area):
	output = ""
	for row in area:
		output += " ".join(row)
		output += "\n"
	print(output)

def	spread(position, area):
	x,y = position
	area[y][x] = 'O'
	new_positions = []
	if area[y][x + 1] == '.':
		new_positions.append((x + 1, y))
	if area[y][x - 1] == '.':
		new_positions.append((x - 1, y))
	if area[y - 1][x] == '.':
		new_positions.append((x, y - 1))
	if area[y + 1][x] == '.':
		new_positions.append((x, y + 1))
	return new_positions

def	fill_oxygen(area):
	positions = [get_start_position(area)]
	minutes = 0
	while len(positions):
		new_positions = []
		for position in positions:
			new_positions.extend(spread(position, area))
		positions = new_positions
		minutes += 1
		visualize(area)
		time.sleep(0.1)
	return minutes - 1

print(fill_oxygen(area))