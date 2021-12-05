from intcode import Intcode

memory = [int(x) for x in open("input").read().split(',') if x != '']

computer = Intcode(memory, None, None, [1])
while not computer.halted:
	computer.run()