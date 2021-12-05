from intcode import Intcode, OPCODE
import itertools

def phase_iterator(settings, memory):
	signal = 0
	for setting in settings:
		output = []
		computer = Intcode(memory, None, None, [setting,signal], output)
		while not computer.halted:
			opcode = computer.run()
			if opcode == OPCODE.WRITE.value:
				break
		signal = output[0]
	return signal

def get_largest_signal(memory):
	permutations = itertools.permutations([0,1,2,3,4])
	largest_signal = 0
	for settings in permutations:
		signal = phase_iterator(settings, memory)
		if signal > largest_signal:
			largest_signal = signal
	return largest_signal

memory = [int(x) for x in open("input").read().split(',') if x != '']

largest_signal = get_largest_signal(memory)
print(largest_signal)
