from intcode import Intcode, OPCODE

class Droid:
	def __init__(self, memory):
		self.inputs = []
		self.outputs = []
		self.software = Intcode(memory, None, None, self.inputs, self.outputs)
	
	def getOutput(self):
		while not self.software.halted:
			operation = self.software.run()
			if operation.opcode == OPCODE.READ.value and self.software.input_index >= len(self.software.inputs):
				command = input()
				command += "\n"
				self.software.inputs.extend([ord(x) for x in command])
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				break
		return self.software.output[-1]

	def run(self):
		while not self.software.halted:
			output = self.getOutput()
			print(chr(output), end="")

memory = [int(x) for x in open("input").read().split(',') if x != '']
droid = Droid(memory)

droid.run()