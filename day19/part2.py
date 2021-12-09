from intcode import Intcode, OPCODE

def scan(x, y, memory):
	# print(x, y)
	outputs = []
	computer = Intcode(memory, None, None, [x,y], outputs)

	while not computer.halted:
		operation = computer.run()
		operation()
		if operation.opcode == OPCODE.WRITE.value:
			break
	return outputs[0]

memory = [int(x) for x in open("input").read().split(',') if x != '']

inputs = []
outputs = []

pulled = 0

area = [[]]

for y in range(1000,1300):
	for x in range(1000):
		result = scan(x, y, memory)
		visual = '.' if not result else '#'
		area[-1].append(visual)
	area.append([])

with open("beam", 'w') as f:
	for line in area:
		f.write("".join(line))
		f.write("\n")
