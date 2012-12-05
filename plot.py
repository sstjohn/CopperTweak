#import hpav
import matplotlib.pyplot as plt
from time import sleep

if __name__ == "__main__":
        fig = plt.figure(figsize=(8,6), dpi=80)
        ax = fig.add_subplot(111)
	X = []
	Y = []
        for i in range(0, 120):
		X.append(i)
		Y.append(i ** 2)
	fig.plot(X, Y, "-")
	fig.show()
