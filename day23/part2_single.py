from intcode import Intcode, OPCODE
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
		self.computers = []
		self.address_index = 0
		self.software = software
		self.nat_packet = None
	
	def add_computer(self):
		computer = Computer(self.software, self.address_index)

		self.address_index += 1
		self.computers.append(computer)

	def handle_packet(self, sender, address, packet):
		if address == 255:
			print(f"NAT_PACKET SET BY {sender}", packet[0], packet[1])
			self.nat_packet = packet
		else:
			print(f"PACKET FROM {sender} to {address}:", packet[0], packet[1])
			self.computers[address].queue.append(packet)

	def is_idle(self, computer):
		if len(computer.queue):
			return False
		if computer.empty_receive < 1:
			return False
		return True

	def run(self):
		y_list = []
		while not all([x.software.halted == True for x in self.computers]):
			for computer in self.computers:
				computer.run(network)
			if self.nat_packet and all([self.is_idle(x) for x in self.computers]):
				print(f"SENDING NAT PACKET", self.nat_packet[0],self.nat_packet[1])
				# if len(y_list) and y_list[-1] == self.nat_packet[1]:
				if self.nat_packet[1] in y_list:
					print("REPEAT Y", self.nat_packet[1])
					exit()
				self.computers[0].queue.append(self.nat_packet)
				y_list.append(self.nat_packet[1])

class Computer:
	def __init__(self, memory, address):
		self.queue = []
		self.address = address
		self.inputs = []
		self.inputs.append(self.address)
		self.outputs = []
		self.status = Status.IDLE.value
		self.software = Intcode(memory, None, None, self.inputs, self.outputs)
		self.output_counter = 0
		self.empty_receive = 0

	def supply_packet(self):
		if self.software.input_index < len(self.software.inputs):
			# if self.software.inputs[self.software.input_index] == -1:
			# 	self.status = Status.IDLE.value
			return
		if len(self.queue):
			x, y = self.queue[-1]
			self.queue = self.queue[:-1]
			self.inputs.append(x)
			self.inputs.append(y)
			self.empty_receive = 0
		else:
			self.inputs.append(-1)
			self.empty_receive += 1
			self.status = Status.IDLE.value

	def prepare_packet(self):
		address = self.outputs[-3]
		x = self.outputs[-2]
		y = self.outputs[-1]
		self.status = Status.BUSY.value
		return (address, (x,y))

	def run(self, network):
		while not self.software.halted:
			operation = self.software.run()
			if operation.opcode == OPCODE.READ.value:
				self.supply_packet()
			operation()
			if operation.opcode == OPCODE.WRITE.value:
				self.output_counter += 1
				if self.output_counter and self.output_counter % 3 == 0:
					address, packet = self.prepare_packet()
					network.handle_packet(self.address, address, packet)
			if operation.opcode == OPCODE.WRITE.value or operation.opcode == OPCODE.READ.value:
				return




software = [int(x) for x in open("input").read().split(',') if x != '']

network = Network(software)

for _ in range(50):
	network.add_computer()

network.run()
