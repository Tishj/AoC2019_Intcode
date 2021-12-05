from intcode import OPCODE, Intcode
from enum import Enum

class Color(Enum):
	BLACK = 0
	WHITE = 1

class Direction(Enum):
	UP = 0
	RIGHT = 90
	DOWN = 180
	LEFT = 270

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def move(self, direction):
		if direction == Direction.UP.value:
			self.y -= 1
		elif direction == Direction.RIGHT.value:
			self.x += 1
		elif direction == Direction.DOWN.value:
			self.y += 1
		else:
			self.x -= 1

class HullPaintingRobot:
	def __init__(self, memory, inputs, outputs):
		self.inputs = inputs
		self.outputs = outputs
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.panels = dict()

		self.direction = Direction.UP.value
		self.position = Position(0, 0)
	
	def getOutput(self):
		opcode = None
		while opcode != OPCODE.WRITE.value:
			opcode = self.computer.run()
		return self.outputs[-1]

	def turn(self, direction):
		self.direction = (self.direction + direction) % 360
		if self.direction < 0:
			self.direction = 360 - self.direction

	def readCurrentColor(self):
		position = (self.position.y, self.position.x)
		color = Color.BLACK.value
		if position in self.panels:
			color = self.panels[position]
		return color

	def convertRawDirection(self, rawDirection):
		return -90 if rawDirection == 0 else 90

#paint, turn, move
	def run(self):
		while not self.computer.halted:
			# Provide the color of the panel the Robot is currently on
			currentColor = self.readCurrentColor()
			self.computer.inputs.append(currentColor)

			# Get output from the robot:
			# Color to paint the current panel
			color = self.getOutput()
			# Direction to turn the robot in
			directionToTurn = self.convertRawDirection(self.getOutput())

			# Update the color of the current panel
			self.panels[(self.position.y, self.position.x)] = color
			# Turn the robot
			self.turn(directionToTurn)
			# Move into the new direction
			self.position.move(self.direction)

memory = [int(x) for x in open("input").read().split(',') if x != '']

memory.extend([0 for i in range(1000000)])

inputs = []
outputs = []
robot = HullPaintingRobot(memory, inputs, outputs)
robot.run()

print(len(list(robot.panels)))
