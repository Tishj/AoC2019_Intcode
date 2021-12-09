from intcode import Intcode, OPCODE
from multiprocessing import Process, Pipe, Queue
import sys
from enum import Enum
import time

class Status(Enum):
	IDLE = 0
	BUSY = 1
	CRASH = 2

class Network:
	def __init__(self, software):
		self.status = Status.IDLE.value
		self.pipes = []
		self.queues = []
		self.processes = []
		self.computers = []
		self.address_index = 0
		self.software = software
		self.nat_queue = Queue()
	
	def add_computer(self):
		pipe = Pipe()
		queue = Queue()
		nat_queue = self.nat_queue if self.address_index == 0 else None
		computer = Computer(self.software, self.address_index, queue, pipe[1], nat_queue)
		process = Process(target=computer.run, args=())

		self.address_index += 1
		self.pipes.append(pipe[0])
		self.queues.append(queue)
		self.computers.append(computer)
		self.processes.append(process)

	def start(self):
		for process in self.processes:
			process.start()

	def run(self):
		status = [Status.IDLE.value for _ in range(len(self.pipes))]
		nat_packet = None
		while True:
			for i,pipe in enumerate(self.pipes):
				if pipe.poll():
					address, packet = pipe.recv()
					if address == 255:
						# print(f"NAT PACKET SET BY {i}:", packet[0],packet[1])
						nat_packet = packet
					elif address == i:
						status[i] = Status.IDLE.value
					else:
						status[i] = Status.BUSY.value
						# print(f"PACKET FROM {i} to {address}:", packet[0], packet[1])
						self.queues[address].put(packet)
						self.status = Status.BUSY.value
			if nat_packet and self.status != Status.IDLE.value and all([x == Status.IDLE.value for x in status]):
				self.status = Status.IDLE.value
				# print(f"SENDING NAT PACKET", nat_packet[0],nat_packet[1])
				self.nat_queue.put(nat_packet)
				time.sleep(0.1)

	def stop(self):
		for process in self.processes:
			process.join()

class Computer:
	def __init__(self, memory, address, queue: Queue, pipe, nat_queue = None):
		self.y_list = []
		self.nat_queue = nat_queue
		self.queue = queue
		self.pipe = pipe
		self.address = address
		self.inputs = []
		self.inputs.append(self.address)
		self.outputs = []
		self.status = Status.IDLE.value
		self.software = Intcode(memory, None, None, self.inputs, self.outputs)

	def supply_packet(self):
		if self.nat_queue and not self.nat_queue.empty():
			x, y = self.nat_queue.get(False)
			print("RECEIVED NAT_PACKET:", x, y)
			if len(self.y_list) and self.y_list[-1] == y:
				print("REPEAT Y:", y)
			self.y_list.append(y)
			self.inputs.append(x)
			self.inputs.append(y)
		
		elif not self.queue.empty():
			x, y = self.queue.get(False)
			self.inputs.append(x)
			self.inputs.append(y)
		else:
			self.inputs.append(-1)
			if self.status != Status.IDLE.value:
				self.pipe.send((self.address, Status.IDLE.value))
			self.status = Status.IDLE.value

	def send_packet(self):
		address = self.outputs[-3]
		x = self.outputs[-2]
		y = self.outputs[-1]

		self.pipe.send((address, (x, y)))
		self.status = Status.BUSY.value

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


software = [int(x) for x in open("input").read().split(',') if x != '']

network = Network(software)

for _ in range(50):
	network.add_computer()

network.start()
network.run()

network.stop()