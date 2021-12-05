from intcode import Intcode

lines = [int(x) for x in open("input").read().split(',') if x != '']
computer = Intcode(lines, 12, 2)

while not computer.halted:
	computer.run()
print(computer.memory[0])