from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 子图画布方式画图


def draw(x_data, y_data, title="", xlable="", ylable=""):
    # 准备画布,设置属性
    figure = plt.figure(title)
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(title)
    axes.set_ylabel(ylable)
    axes.set_xlabel(xlable)
    # 稀疏Y轴
    ymajorLocator = MultipleLocator(10000)
    axes.yaxis.set_major_locator(ymajorLocator)
    # 画折线
    axes.plot(x_data, y_data, color='tab:blue')
    # 显示
    plt.show()

# 原始画图方式


def plt_draw(x_data, y_data, title="", xlable="", ylable=""):
    plt.cla()
    # 准备绘制数据
    # "g" 表示红色，marksize用来设置'D'菱形的大小
    plt.plot(x_data, y_data, "g", marker='D', markersize=2)
    # 绘制坐标轴标签
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.title(title)
    plt.pause(0.1)
