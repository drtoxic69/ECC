import matplotlib.pyplot as plt
import numpy as np


def plot_curve(a, b):

    y, x = np.ogrid[-10:10:100j, -10:10:100j]

    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    plt.grid()
    plt.show()


if __name__ == "__main__":
    plot_curve(0, 7)
