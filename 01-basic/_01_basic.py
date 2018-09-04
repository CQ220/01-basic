import matplotlib.pyplot as plt

# 定义 x 和 y 坐标轴上的点
x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

# 使用 plot() 函数功能绘制线条
plt.plot(x, y)

# 修改 matplotlib 的字体设置，解决无法显示中文问题
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #制定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像时负号'-'显示为方块

# 在图形上添加文本
plt.xlabel('x 坐标轴') # x轴
plt.ylabel('y 坐标轴') # y轴
plt.annotate('我是注释', xy = (2, 5), xytext=(2, 10), arrowprops=dict(facecolor='black', shrink = 0.01))

# 显示图像
plt.show()