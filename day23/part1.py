from intcode import Intcode, OPCODE
from multiprocessing import Process, Pipe, Queue
import sys

class Computer:
	def __init__(self, memory, address, queue: Queue, pipe):
		self.queue = queue
		self.pipe = pipe
		self.address = address
		self.inputs = []
		self.inputs.append(self.address)
		self.outputs = []
		self.software = Intcode(memory, None, None, self.inputs, self.outputs)

	def supply_packet(self):
		if not self.queue.empty():
			x, y = self.queue.get(False)
			self.inputs.append(x)
			self.inputs.append(y)
		else:
			self.inputs.append(-1)

	def send_packet(self):
		address = self.outputs[-3]
		x = self.outputs[-2]
		y = self.outputs[-1]

		if address == 255:
			print("ADDRESS 255 -", x, y)

		self.pipe.send((address, (x, y)))


	def run(self):
		output_counter = 0
		while not self.software.halted:
			operation = self.software.run()
			if operation.opcode == OPCODE.READ.value:
				self.supply_packet()
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				output_counter += 1
				if output_counter % 3 == 0:
					self.send_packet()
					output_counter = 0


memory = [int(x) for x in open("input").read().split(',') if x != '']

pipes = [Pipe() for _ in range(50)]
queues = [Queue() for _ in range(50)]
computers = [Computer(memory, i, queues[i], pipes[i][1]) for i in range(50)]

processes = [Process(target=computers[i].run, args=()) for i in range(50)]

for process in processes:
	process.start()

while True:
	for pipe in [x[0] for x in pipes]:
		if pipe.poll():
			address, packet = pipe.recv()
			queues[address].put(packet)

for process in processes:
	process.join()