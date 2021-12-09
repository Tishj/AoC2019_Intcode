lines = open("beam_1000").read().split()

# for line in lines:
# 	print(line)

size = 100

location = None

for y, line in enumerate(lines):
	start_beam = line.find('#')
	end_beam = line.rfind('#')
	if end_beam - start_beam < size:
		continue
	location_x = end_beam - size + 1
	try:
		if lines[y + size - 1][location_x] == '#':
			location = (location_x,y)
			print(location_x * 10000 + y)
			break
	except IndexError:
		continue

if location:
	for i in range(location[1], location[1] + 10):
		new_line = ""
		square = range(location[0], location[0] + 10)
		for j, item in enumerate(lines[i]):
			if j in square:
				new_line += 'O'
			else:
				new_line += item
		lines[i] = new_line

	for line in lines:
		print(line)

	print(location[0] * 10000 + location[1])
else:
	print("No dice")