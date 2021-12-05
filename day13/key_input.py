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
			print("RIGHT")
		elif k == '\x1b[D':
			print("LEFT")
		elif k == '\x1b[A':
			print("UP")

def main():
		for i in range(0,10):
				get()

if __name__=='__main__':
		main()