import hpav
import pylab
from time import sleep

PLOT_TIME = 120

class ToneMap():
	def __init__(self, index, x):
		self.x = x
		self.y = []
		self.index = index
		self.line, = pylab.plot(self.x, self.y)

	def update(self):
		try:
			self.y.append(hpav.get_def_tmi_score(self.index))
		except:
			self.y.append(0)
		self.line.set_xdata(self.x)
		self.line.set_ydata(self.y)

if __name__ == "__main__":
	x = []
	pylab.ion()
	pylab.axis([0, PLOT_TIME, 0, 2048])
	tms = [ToneMap(i, x) for i in range(0,10)]
        for i in range(0, PLOT_TIME * 5):
		x.append(i / 5)
		for tm in tms:
			tm.update()
		pylab.draw()
		sleep(1 / 5)
