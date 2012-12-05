#import hpav
import matplotlib.pyplot as plt
from time import sleep

if __name__ == "__main__":
	X = []
	Y = []
        for i in range(0, 120):
		X.append(i)
		Y.append(i ** 2)
	plt.plot(X, Y, "-")
	plt.show()
