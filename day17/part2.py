from intcode import Intcode, OPCODE

class ASCII:
	counter = 0
	def __init__(self, memory, inputs, outputs):
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.computer.memory[0] = 2
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
		last_output = None
		while not self.computer.halted:
			output = self.getOutput()
			if output == 10:
				self.counter += 1
				self.map.append([])
				if last_output == 10:
					self.visualize()
					self.map = [[]]
			else:
				self.map[-1].append(chr(output))
			last_output = output

	def visualize(self):
		output = ""
		for line in self.map:
			output += " ".join(line)
			output += "\n"
		print(output)


def assemble_routine():
	routine = []
	routine.extend(list("A,B,B,A,C,A,C,A,C,B\n"))
	routine.extend(list("L,6,R,12,R,8\n"))
	routine.extend(list("R,8,R,12,L,12\n"))
	routine.extend(list("R,12,L,12,L,4,L,4\n"))
	routine.extend(list("y\n"))
	return routine


memory = [int(x) for x in open("input").read().split(',') if x != '']
memory.extend([0 for _ in range(10000000)])

inputs = []
# with open("inputs.json", 'r') as f:
# 	inputs.extend(json.load(f))
routine = assemble_routine()

inputs.extend([ord(x) for x in routine])

outputs = []
robot = ASCII(memory, inputs, outputs)
robot.write()
robot.visualize()

print(robot.computer.output[-1])