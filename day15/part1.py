from intcode import Intcode, OPCODE
from enum import Enum
import sys,tty,termios
import json
import random
import signal
import time

randomize = False

def signal_handler(signum, frame):
	global randomize
	randomize = not randomize

class _Getch:
	def __call__(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(3)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

def get():
	inkey = _Getch()
	while(1):
			k=inkey()
			if k!='':break
	if k == '\x1b[C':
		return 4
	elif k == '\x1b[D':
		return 3
	elif k == '\x1b[B':
		return 2
	elif k == '\x1b[A':
		return 1
	elif k == '\x1b[H':
		return 0
	elif k == '\x1b[3':
		return 10
	else:
		return -1

class Object(Enum):
	UNDISCOVERED = 0
	EMPTY = 1
	WALL = 2
	OXYGEN_SYSTEM = 3

class Status(Enum):
	WALLHIT = 0
	MOVED = 1
	FOUND = 2

class Movement(Enum):
	NORTH = 1
	SOUTH = 2
	WEST = 3
	EAST = 4

def saveMap(droid):
	converted = dict()
	for key, value in droid.area.items():
		converted[str(key)] = value
	with open("map.json", 'w') as f:
		json.dump(converted, f)
	with open("inputs.json", 'w') as f:
		json.dump(droid.computer.inputs, f)
	print("Succesfully saved to 'map.json'")

class RepairDroid:
	def __init__(self, memory, inputs, outputs):
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.area = dict()
		self.position = (0,0)
		self.found = False
		self.randomize = True
		self.moves = []

	def getObjectAtCoordinate(self, position):
		if position in self.area:
			return self.area[position]
		else:
			return Object.UNDISCOVERED.value

	def surroundings(self):
		position = dict()
		x,y = self.position
		position[Movement.EAST.value] = (x + 1, y)
		position[Movement.NORTH.value] = (x, y - 1)
		position[Movement.SOUTH.value] = (x, y + 1)
		position[Movement.WEST.value] = (x - 1, y)
		return position

	def visualize(self):
		area = [[' ' for _ in range(12)] for _ in range(12)]
		start_x = self.position[0] - 5
		start_y = self.position[1] - 5
		for x in range(start_x, start_x + 11):
			for y in range(start_y, start_y + 11):
				position = (x,y)
				if position in self.area:
					visual = ' '
					if x == self.position[0] and y == self.position[1]:
						visual = 'P'
					elif self.area[position] == Object.WALL.value:
						visual = '#'
					elif self.area[position] == Object.EMPTY.value:
						visual = '.'
					area[y - start_y][x - start_x] = visual

		output = ""
		for line in area:
			output += " ".join(line)
			output += "\n"
		print(output)
		print("Player:", self.position)

	def getReverseMove(self, move):
		if move == Movement.EAST.value:
			return Movement.WEST.value
		if move == Movement.WEST.value:
			return Movement.EAST.value
		if move == Movement.NORTH.value:
			return Movement.SOUTH.value
		if move == Movement.SOUTH.value:
			return Movement.NORTH.value

	# This makes my brain hurt
	def determineMove(self):
		# global randomize
		# if randomize:
		# 	return random.choices([1,2,3,4])[0]
		# else:
		move = get()
		if move == 0:
			saveMap(self)
			return self.determineMove()
		elif move == -1:
			exit()
		return move
		# surroundings = self.position.surroundings()

		# choice = None
		# for key, value in surroundings.items():
		# 	tile = self.getObjectAtCoordinate(value)
		# 	if tile == Object.WALL.value:
		# 		continue
		# 	elif tile == Object.UNDISCOVERED.value:
		# 		choice = key
		# 	elif tile == Object.OXYGEN_SYSTEM.value:
		# 		return key
		# if choice == None:
		# 	choice = self.getReverseMove(self.moves[-1])
		# 	self.moves.pop()
		# else:
		# 	self.moves.append(choice)
		# return choice

	def getOutput(self):
		while not self.computer.halted:
			operation = self.computer.run()
			if operation.opcode == OPCODE.READ.value:
				self.computer.inputs.append(self.determineMove())
				time.sleep(0.1)
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				break
		return self.computer.output[-1]

	def remoteControl(self):
		statusReport = self.getOutput()
		print(statusReport)
		direction = self.surroundings()[self.computer.inputs[-1]]
		if statusReport == Status.FOUND.value:
			self.found = True
			self.position = direction
			self.area[self.position] = Object.OXYGEN_SYSTEM.value
		elif statusReport == Status.MOVED.value:
			if direction not in self.area or self.area[direction] != Object.WALL.value:
				self.position = direction
				self.area[self.position] = Object.EMPTY.value
		elif statusReport == Status.WALLHIT.value:
			self.area[direction] = Object.WALL.value
		else:
			print("INVALID OUTPUT RETURNED")
			exit()

	def loop(self):
		while not self.computer.halted and not self.found:
			self.visualize()
			self.remoteControl()

memory = [int(x) for x in open("input").read().split(',') if x != '']
memory.extend([0 for _ in range(10000000)])

inputs = []
with open("inputs.json", 'r') as f:
	inputs.extend(json.load(f))
outputs = []
droid = RepairDroid(memory, inputs, outputs)


while not droid.computer.halted and not droid.found:
	droid.loop()

saveMap(droid)
