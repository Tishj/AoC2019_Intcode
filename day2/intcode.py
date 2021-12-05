from enum import Enum

class OPCODE(Enum):
	ADD = 1
	MULT = 2
	READ = 3
	WRITE = 4
	HALT = 99

class PARAMETER_MODE(Enum):
	POSITION = 0
	IMMEDIATE = 1

# Base class for an Operation (ADD, MULT, ..)
class Operation:
	def __init__(self, computer, parameter_modes, argument_count):
		self.arguments = list()
		for i,mode in enumerate(parameter_modes):
			if i >= argument_count:
				break
			argument = computer.memory[computer.instruction_pointer + i + 1]
			self.arguments.append((int(mode), argument))
		computer.instruction_pointer += argument_count + 1

	def getArgument(self, computer, n):
		mode, arg = self.arguments[n]
		if mode == PARAMETER_MODE.IMMEDIATE.value:
			return arg
		elif mode == PARAMETER_MODE.POSITION.value:
			return computer.memory[arg]
		else:
			print("INVALID PARAMETER MODE FOR GET-ARGUMENT")
			exit()
	
	def setArgument(self, computer, n, value):
		mode, arg = self.arguments[n]
		if mode == PARAMETER_MODE.IMMEDIATE.value:
			print("INVALID PARAMETER MODE FOR SET-ARGUMENT")
			exit()
		elif mode == PARAMETER_MODE.POSITION.value:
			computer.memory[arg] = value
		else:
			print("INVALID PARAMETER MODE FOR SET-ARGUMENT")
			exit()

class Add(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, 3)
		self.setArgument(computer, 2, self.getArgument(computer, 0) + self.getArgument(computer, 1))

class Multiply(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, 3)
		self.setArgument(computer, 2, self.getArgument(computer, 0) * self.getArgument(computer, 1))

# class Read(Operation):
# 	def __init__(self, computer, instruction):
# 		super().__init__(computer, instruction)
# 		computer.halted = True
# 		computer.instruction_pointer += len(self.arguments)

class Halt(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, 0)
		computer.halted = True

class Intcode:
	def __init__(self, memory, noun, verb):
		self.halted = False
		self.instruction_pointer = 0
		self.memory = memory.copy()
		self.memory[1] = noun
		self.memory[2] = verb

	def run(self):
		pointer = self.instruction_pointer
		instruction_string = str(self.memory[pointer]).zfill(5)
		opcode = int(instruction_string[3:5])
		parameter_modes = instruction_string[0:3]
		if opcode == OPCODE.ADD.value:
			Add(self, parameter_modes)
		elif opcode == OPCODE.MULT.value:
			Multiply(self, parameter_modes)
		elif opcode == OPCODE.HALT.value:
			Halt(self, parameter_modes)
		else:
			print("INVALID OPCODE")
			exit()