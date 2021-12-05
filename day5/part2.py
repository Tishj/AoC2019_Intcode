from intcode import Intcode

memory = [int(x) for x in open("input").read().split(',') if x != '']

computer = Intcode(memory, None, None, [5])
while not computer.halted:
	computer.run()