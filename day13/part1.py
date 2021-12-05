from intcode import Intcode, OPCODE
from enum import Enum

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

class Empty(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.EMPTY.value, x, y)

class Wall(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.WALL.value, x, y)

class Block(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.BLOCK.value, x, y)

class Paddle(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.PADDLE.value, x, y)

class Ball(Tile):
	def __init__(self, x, y):
		super().__init__(TileID.BALL.value, x, y)

class Arcade:
	def __init__(self, memory, inputs, outputs):
		self.computer = Intcode(memory, None, None, inputs, outputs)
		self.tiles = []

	def getOutput(self):
		opcode = None
		while opcode != OPCODE.WRITE.value:
			operation = self.computer.run()
			opcode = operation.opcode
			operation()
		return self.computer.output[-1]

	def draw(self):
		x = self.getOutput()
		y = self.getOutput()
		tileID = self.getOutput()

		if tileID == TileID.EMPTY.value:
			self.tiles.append(Empty(x,y))
		elif tileID == TileID.WALL.value:
			self.tiles.append(Wall(x,y))
		elif tileID == TileID.BLOCK.value:
			self.tiles.append(Block(x,y))
		elif tileID == TileID.PADDLE.value:
			self.tiles.append(Paddle(x,y))
		elif tileID == TileID.BALL.value:
			self.tiles.append(Ball(x,y))
		else:
			print("INVALID TILEID")
			exit()
	
	def run(self):
		while not self.computer.halted:
			self.draw()

memory = [int(x) for x in open("input").read().split(',') if x != '']
memory.extend([0 for _ in range(10000000)])

inputs = []
outputs = []
arcade = Arcade(memory, inputs, outputs)
arcade.run()

block_tiles = sum([1 for tile in arcade.tiles if tile.id == TileID.BLOCK.value])
print(block_tiles)
