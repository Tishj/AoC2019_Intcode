from intcode import Intcode, OPCODE
from enum import Enum
import time
import json
import os

import sys,tty,termios
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
		return 1
	elif k == '\x1b[D':
		return -1
	else:
		return 0

class TileID(Enum):
	EMPTY = 0
	WALL = 1
	BLOCK = 2
	PADDLE = 3
	BALL = 4

class Tile:
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y

class Move(Enum):
	NEUTRAL = 0
	RIGHT = 1
	LEFT = -1

class Empty(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.EMPTY.value, x, y)
		self.visual = ' '

class Wall(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.WALL.value, x, y)
		self.visual = '#'

class Block(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.BLOCK.value, x, y)
		self.visual = 'X'

class Paddle(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.PADDLE.value, x, y)
		self.visual = '_'

class Ball(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.BALL.value, x, y)
		self.visual = 'O'

class Arcade:
	def __init__(self, memory, inputs, outputs, savestate = None, ai=False):
		if ai:
			self.ai = ArcadeAI(self)
		else:
			self.ai = None
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.computer.memory[0] = 2
		self.save_len = 0 if not savestate else len(savestate)
		if savestate:
			inputs.extend(savestate)
		self.tiles = dict()
		self.screen = [[' ' for _ in range(45)] for _ in range(24)]
		self.score = 0
		self.score_history = []

	def getOutput(self):
		opcode = None
		while opcode != OPCODE.WRITE.value:
			operation = self.computer.run()
			if not operation:
				return None
			opcode = operation.opcode
			if opcode == OPCODE.READ.value:
				self.draw()
				if self.computer.input_index >= self.save_len:
					if self.ai:
						self.computer.inputs.append(self.ai.move())
					else:
						self.computer.inputs.append(get())
					# time.sleep(0.1)
				operation()
			else:
				operation()

		return self.computer.output[-1]

	def updateScreen(self, tile):
		self.screen[tile.y][tile.x] = tile.visual

	def read(self):
		x = self.getOutput()
		y = self.getOutput()
		tileID = self.getOutput()

		# Weird error
		if x == None or y == None or tileID == None:
			return

		if x == -1 and y == 0:
			self.score_history.append(self.score)
			self.score = tileID
			return
		position = (x,y)
		if tileID == TileID.EMPTY.value:
			tile = Empty(x,y)
			self.tiles[position] = tile
		elif tileID == TileID.WALL.value:
			tile = Wall(x,y)
			self.tiles[position] = tile
		elif tileID == TileID.BLOCK.value:
			tile = Block(x,y)
			self.tiles[position] = tile
		elif tileID == TileID.PADDLE.value:
			tile = Paddle(x,y)
			self.tiles[position] = tile
		elif tileID == TileID.BALL.value:
			tile = Ball(x,y)
			self.tiles[position] = tile
		else:
			print("INVALID TILEID")
			exit()
		self.updateScreen(tile)
	
	def draw(self):
		output = ""
		for line in self.screen:
			output += " ".join(line)
			output += "\n"
		print(output)
		print("".join([' ' for _ in range(32)]) + "SCORE: " + str(self.score))
		if self.ai:
			print(self.ai.lastMove())

	def run(self):
		while not self.computer.halted:
			self.read()

class ArcadeAI:
	def __init__(self, arcade):
		self.ball_trajectory = 1
		self.arcade = arcade
		self.last_move = None
		self.oldBallPosition = None

	def lastMove(self):
		if self.last_move == None:
			return "None"
		elif self.last_move == Move.NEUTRAL.value:
			return "NEUTRAL"
		elif self.last_move == Move.LEFT.value:
			return 'LEFT'
		else:
			return "RIGHT"

	def updateTrajectory(self, ball):
		if self.oldBallPosition == None:
			self.ball_trajectory = 1
			return
		difference = ball[0] - self.oldBallPosition[0]
		if difference > 0:
			self.ball_trajectory = 1
		else:
			self.ball_trajectory = -1
		print("Difference:", difference, self.ball_trajectory)

	def move(self):
		position = self.getPosition(TileID.PADDLE.value)
		ballPosition = self.getPosition(TileID.BALL.value)
		move = None

		self.updateTrajectory(ballPosition)

		if self.oldBallPosition and ballPosition[1] < self.oldBallPosition[1]:
			print("MOVING UP")
			self.ball_trajectory *= -1
			difference = position[0] - ballPosition[0]
			if difference == 0:
				move = Move.NEUTRAL.value
			elif difference > 0:
				move = Move.LEFT.value
			else:
				move = Move.RIGHT.value
		else:
			estimated_collision_point = ballPosition[0] + (self.ball_trajectory * (position[1] - ballPosition[1]))
			print("ESTIMATED_COLLISION", estimated_collision_point)
			print("MY_X", position[0])
			print("BALL_X", ballPosition[0])
			difference = position[0] - estimated_collision_point
			if difference == 0:
				move = Move.NEUTRAL.value
			elif difference > 0:
				move = Move.LEFT.value
			else:
				move = Move.RIGHT.value
		self.oldBallPosition = ballPosition
		self.last_move = move
		return move

	def getPosition(self, tileID):
		for key, value in self.arcade.tiles.items():
			if value.id == tileID:
				return key
		return None

memory = [int(x) for x in open("input").read().split(',') if x != '']
memory.extend([0 for _ in range(10000000)])

save = None
# if os.path.exists("./keys"):
# 	with open("./keys", 'r') as f:
# 		save = json.load(f)
inputs = []
# inputs.extend([0 for _ in range(100)])
outputs = []
arcade = Arcade(memory, inputs, outputs, save, True)
arcade.run()

with open("./keys", 'w') as f:
	json.dump(arcade.computer.inputs, f, indent=4)
if save != None:
	with open("./score", 'w') as f:
		json.dump(arcade.score_history, f, indent=4)
arcade.draw()

print(arcade.score)