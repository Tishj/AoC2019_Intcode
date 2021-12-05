from intcode import Intcode

memory = [int(x) for x in open("input").read().split(',') if x != '']

memory.extend([0 for i in range(1000000)])

output = []
computer = Intcode(memory, None, None, [1], output)
while not computer.halted:
	computer.run()

print(output)
