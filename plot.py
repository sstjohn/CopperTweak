#import hpav
import matplotlib.pyplot as plt
from time import sleep

if __name__ == "__main__":
	x = []
	y = []
	line, = plt.plot(x, y, '-')
        for i in range(0, 120):
		x.append(i)
		y.append(i ** 2)
		line.set_xdata(x)
		line.set_ydata(y)
		plt.draw()
		sleep(1)
