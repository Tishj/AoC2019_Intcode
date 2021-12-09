from intcode import Intcode, OPCODE

class SpringDroid:
	def __init__(self, memory):
		self.inputs = []
		self.outputs = []
		self.computer = Intcode(memory, None, None, self.inputs, self.outputs)
	
	def getOutput(self):
		while not self.computer.halted:
			operation = self.computer.run()
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				break
		return self.outputs[-1]
	
	def loadScript(self, scriptFile):
		with open(scriptFile, 'r') as f:
			self.inputs.extend(ord(x) for x in f.read())
	
	def run(self):
		while not self.computer.halted:
			output = self.getOutput()
			try:
				print(chr(output), end="")
			except:
				print("ANSWER:", output)

memory = [int(x) for x in open("input").read().split(',') if x != '']

droid = SpringDroid(memory)
droid.loadScript("script_part2.ss")
droid.run()