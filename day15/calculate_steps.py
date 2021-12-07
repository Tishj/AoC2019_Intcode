import json
import sys

sys.setrecursionlimit(1000)

area = list()
for line in open("visualized").read().split("\n"):
	area.append([x[0] for x in [line[i:i+2] for i in range(0, len(line), 2)]])

def get_start_position(area):
	for y, line in enumerate(area):
		for x, char in enumerate(line):
			if area[y][x] == 'S':
				return (x,y)

def travel(position, area, path_lengths, steps = 0):
	# print(steps)
	# print(area[y][x])
	x,y = position
	if area[y][x] == 'E':
		path_lengths.append(steps)
		with open("shortest_route", 'w') as f:
			for line in area:
				f.write(" ".join(line))
				f.write("\n")
			# exit()
		return
	if area[y][x] != '.' and area[y][x] != 'S':
		return
	area[y][x] = chr((steps % 26) + ord('A'))
	travel((x,y+1), area.copy(), path_lengths, steps + 1)
	travel((x,y-1), area.copy(), path_lengths, steps + 1)
	travel((x+1,y), area.copy(), path_lengths, steps + 1)
	travel((x-1,y), area.copy(), path_lengths, steps + 1)

path_lengths = []
travel(get_start_position(area), area.copy(), path_lengths)

print(path_lengths)
print(min(path_lengths))