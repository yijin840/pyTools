# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import time
import numpy as np
from numpy.random import rand


plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
fig.canvas.manager.set_window_title("内存占用分析")
def draw(val):
    plt.plot(val)
    plt.ylabel('some numbers')
    plt.show()
def main():
    lis = [1,2,3,4,5]
    draw(lis)
main()