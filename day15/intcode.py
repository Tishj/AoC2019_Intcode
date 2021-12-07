from enum import Enum

class OPCODE(Enum):
	ADD = 1
	MULT = 2
	READ = 3
	WRITE = 4
	JUMPIFTRUE = 5
	JUMPIFFALSE = 6
	LESSTHAN = 7
	EQUALS = 8
	OFFSET = 9
	HALT = 99

class PARAMETER_MODE(Enum):
	POSITION = 0
	IMMEDIATE = 1
	RELATIVE = 2

# Base class for an Operation (ADD, MULT, ..)
class Operation:
	def __init__(self, computer, parameter_modes, opcode, argument_count):
		self.opcode = opcode
		self.computer = computer
		self.arguments = list()
		for i,mode in enumerate(parameter_modes[::-1]):
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
		elif mode == PARAMETER_MODE.RELATIVE.value:
			return computer.memory[arg + computer.relative_pointer]
		else:
			print("INVALID PARAMETER MODE FOR GET-ARGUMENT")
			exit()
	
	def setArgument(self, computer, n, value):
		mode, arg = self.arguments[n]
		if mode == PARAMETER_MODE.IMMEDIATE.value:
			print("INVALID PARAMETER MODE FOR SET-ARGUMENT", mode)
			exit()
		elif mode == PARAMETER_MODE.POSITION.value:
			computer.memory[arg] = value
		elif mode == PARAMETER_MODE.RELATIVE.value:
			computer.memory[arg + computer.relative_pointer] = value
		else:
			print("INVALID PARAMETER MODE FOR SET-ARGUMENT", mode)
			exit()

class Add(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.ADD.value, 3)
	def __call__(self):
		self.setArgument(self.computer, 2, self.getArgument(self.computer, 0) + self.getArgument(self.computer, 1))

class Read(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.READ.value, 1)
	def __call__(self):
		value = self.computer.inputs[self.computer.input_index]
		self.computer.input_index += 1
		self.setArgument(self.computer, 0, value)

class Write(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.WRITE.value, 1)
	def __call__(self):
		self.computer.output.append(self.getArgument(self.computer, 0))

class Multiply(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.MULT.value, 3)
	def __call__(self):
		self.setArgument(self.computer, 2, self.getArgument(self.computer, 0) * self.getArgument(self.computer, 1))

class Halt(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.HALT.value, 0)
	def __call__(self):
		self.computer.halted = True

class Offset(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.OFFSET.value, 1)
	def __call__(self):
		self.computer.relative_pointer += self.getArgument(self.computer, 0)

class JumpIfTrue(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.JUMPIFTRUE.value, 2)
	def __call__(self):
		if self.getArgument(self.computer, 0) != 0:
			self.computer.instruction_pointer = self.getArgument(self.computer, 1)

class JumpIfFalse(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.JUMPIFFALSE.value, 2)
	def __call__(self):
		if self.getArgument(self.computer, 0) == 0:
			self.computer.instruction_pointer = self.getArgument(self.computer, 1)

class LessThan(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.LESSTHAN.value, 3)
	def __call__(self):
		if self.getArgument(self.computer, 0) < self.getArgument(self.computer, 1):
			self.setArgument(self.computer, 2, 1)
		else:
			self.setArgument(self.computer, 2, 0)

class Equals(Operation):
	def __init__(self, computer, parameter_modes):
		super().__init__(computer, parameter_modes, OPCODE.EQUALS.value, 3)
	def __call__(self):
		if self.getArgument(self.computer, 0) == self.getArgument(self.computer, 1):
			self.setArgument(self.computer, 2, 1)
		else:
			self.setArgument(self.computer, 2, 0)

class Intcode:
	def __init__(self, memory, noun, verb, inputs, output):
		self.output = output
		self.inputs = inputs
		self.input_index = 0
		self.halted = False
		self.relative_pointer = 0
		self.instruction_pointer = 0
		self.memory = memory.copy()
		if noun:
			self.memory[1] = noun
		if verb:
			self.memory[2] = verb

	def run(self):
		pointer = self.instruction_pointer
		instruction_string = str(self.memory[pointer]).zfill(5)
		opcode = int(instruction_string[3:5])
		parameter_modes = instruction_string[0:3]
		
		operation = None
		if opcode == OPCODE.ADD.value:
			operation = Add(self, parameter_modes)
		elif opcode == OPCODE.MULT.value:
			operation = Multiply(self, parameter_modes)
		elif opcode == OPCODE.HALT.value:
			operation = Halt(self, parameter_modes)
		elif opcode == OPCODE.READ.value:
			operation = Read(self, parameter_modes)
		elif opcode == OPCODE.WRITE.value:
			operation = Write(self, parameter_modes)
		elif opcode == OPCODE.JUMPIFTRUE.value:
			operation = JumpIfTrue(self, parameter_modes)
		elif opcode == OPCODE.JUMPIFFALSE.value:
			operation = JumpIfFalse(self, parameter_modes)
		elif opcode == OPCODE.LESSTHAN.value:
			operation = LessThan(self, parameter_modes)
		elif opcode == OPCODE.EQUALS.value:
			operation = Equals(self, parameter_modes)
		elif opcode == OPCODE.OFFSET.value:
			operation = Offset(self, parameter_modes)
		else:
			print("INVALID OPCODE:", opcode)
			return None
		return operation
