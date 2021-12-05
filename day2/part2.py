from intcode import Intcode

lines = [int(x) for x in open("input").read().split(',') if x != '']
computer = Intcode(lines, 12, 2)

for noun in range(0, 100):
	for verb in range(0, 100):
		computer = Intcode(lines, noun, verb)
		while not computer.halted:
			computer.run()
			if computer.memory[0] == 19690720:
				print(noun, verb)
				exit()