import matplotlib.pyplot as plt
import numpy as np


def draw(y_list):
    x = np.arange(0, 2048)
    l1 = plt.plot(x, y_list[0:2048], 'r--', label='type1')
    plt.title('The Lasers in Three Conditions')
    plt.xlabel('row')
    plt.ylabel('column')
    plt.savefig('test.jpg')
    plt.legend()
    plt.show()
