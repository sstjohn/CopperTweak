import hpav
import pylab
from time import sleep

PLOT_TIME = 120

if __name__ == "__main__":
	x = [0]
	y0 = [hpav.get_def_tmi_score(0)]
	y1 = [hpav.get_def_tmi_score(1)]
	y2 = [hpav.get_def_tmi_score(2)]
	y3 = [hpav.get_def_tmi_score(3)]
	ylim = y0[0] * 3
	pylab.ion()
	line0, = pylab.plot(x, y0, '-')
	line1, = pylab.plot(x, y1, 'r-')
	line2, = pylab.plot(x, y2, 'b-')
	line3, = pylab.plot(x, y3, 'g-')
	pylab.axis([0, PLOT_TIME, 0, ylim])
        for i in range(1, PLOT_TIME * 5):
		x.append(i / 5)
		y0.append(hpav.get_def_tmi_score(0))
		y1.append(hpav.get_def_tmi_score(1))
		y2.append(hpav.get_def_tmi_score(2))
		y3.append(hpav.get_def_tmi_score(3))
		line0.set_xdata(x)
		line0.set_ydata(y0)
		line1.set_xdata(x)
		line1.set_ydata(y1)
		line2.set_xdata(x)
		line2.set_ydata(y2)
		line3.set_xdata(x)
		line3.set_ydata(y3)
		pylab.draw()
		sleep(1/5)
