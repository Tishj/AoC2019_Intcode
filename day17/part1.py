from intcode import Intcode, OPCODE

class ASCII:
	def __init__(self, memory, inputs, outputs):
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.map = []
		self.map.append([])

	def getOutput(self):
		while not self.computer.halted:
			operation = self.computer.run()
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				break
		return self.computer.output[-1]

	def write(self):
		while not self.computer.halted:
			output = self.getOutput()
			if output == 10:
				self.map.append([])
			else:
				self.map[-1].append(chr(output))

	def visualize(self):
		output = ""
		for line in self.map:
			output += " ".join(line)
			output += "\n"
		print(output)


memory = [int(x) for x in open("input").read().split(',') if x != '']
memory.extend([0 for _ in range(10000000)])

inputs = []
# with open("inputs.json", 'r') as f:
# 	inputs.extend(json.load(f))
outputs = []
robot = ASCII(memory, inputs, outputs)
robot.write()
robot.visualize()

def is_inside_map(position, area):
	x, y = position
	# print(position)
	height = len(area)
	width = len(area[0])
	# print(width, height)
	if x < 0 or x >= width:
		return False
	if y < 0 or y >= height:
		return False
	return True

def is_intersection(position, area):
	x, y = position
	try:
		if not is_inside_map((x + 1, y), area) or area[y][x + 1] != '#':
			return False
		if not is_inside_map((x - 1, y), area) or area[y][x - 1] != '#':
			return False
		if not is_inside_map((x, y + 1), area) or area[y + 1][x] != '#':
			return False
		if not is_inside_map((x, y - 1), area) or area[y - 1][x] != '#':
			return False
	except IndexError:
		return False
	return True

intersections = []
for y, line in enumerate(robot.map):
	for x, item in enumerate(line):
		if item == '#' and is_intersection((x, y), robot.map):
			intersections.append(y * x)

print(sum(intersections))