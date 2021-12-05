from intcode import Intcode, OPCODE
import itertools

def phase_iterator(settings, memory):
	amplifiers = list()
	for i in range(5):
		amplifiers.append(Intcode(memory, None, None, [settings[i]], None))
	for i in range(5):
		amplifiers[i].output = amplifiers[(i + 1) % 5].inputs
	index = 0
	signal = 0
	while not amplifiers[-1].halted:
		# print(amplifiers[index].output)
		opcode = amplifiers[index].run()
		if amplifiers[index].halted == True:
			index = (index + 1) % 5
		elif opcode == OPCODE.WRITE.value:
			signal = amplifiers[index].output[-1]
			index = (index + 1) % 5
			# print("INDEX:", index)
	return signal

def get_largest_signal(memory):
	permutations = itertools.permutations([5,6,7,8,9])
	largest_signal = 0
	for settings in permutations:
		signal = phase_iterator(settings, memory)
		if signal > largest_signal:
			largest_signal = signal
	return largest_signal

memory = [int(x) for x in open("input").read().split(',') if x != '']

largest_signal = get_largest_signal(memory)
print(largest_signal)
