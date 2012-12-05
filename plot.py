import hpav
import pylab
from time import sleep

PLOT_TIME = 120

if __name__ == "__main__":
	x = [0]
	y = [hpav.get_def_tm_score()]
	ylim = y[0] * 3
	pylab.ion()
	line, = pylab.plot(x, y, '-')
	pylab.axis([0, PLOT_TIME, 0, ylim])
        for i in range(1, PLOT_TIME * 5):
		x.append(i / 5)
		y.append(hpav.get_def_tm_score())
		line.set_xdata(x)
		line.set_ydata(y)
		pylab.draw()
		sleep(1/5)
