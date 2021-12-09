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

for y in range(50):
	for x in range(50):
		pulled += scan(x, y, memory)

print(pulled)