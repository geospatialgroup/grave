import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.stats import linregress

# 读取.mat文件
x_data = sio.loadmat('G:/Xu/画图/figure5/x.mat')
y_data = sio.loadmat('G:/Xu/画图/figure5/y_density.mat')

y = y_data['y_density'].squeeze()

# 提取变量
GDP = x_data['x'][:, 12]

x = GDP

# 线性回归拟合参数
# 线性回归拟合
slope, intercept, r_value, p_value, std_err = linregress(x, y)
# slope = 0.4888
# intercept = -6.7583
line = slope * x + intercept  # 拟合线

# 设置 Times New Roman 字体（全局）
plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28

# 绘图
plt.figure(figsize=(8, 6))  # 可选：设置图形大小

# 绘制高透明度的深蓝色散点
plt.scatter(x, y, s=80, color='#a6cee3', alpha=0.7, edgecolors='#1f78b4')  # alpha 控制透明度

# 绘制灰色拟合线
plt.plot(x, line, color='#fb8072', linewidth=2)

# 设置标签
plt.xlabel('Distance to districts (°)', fontsize=28)
plt.ylabel('Graves density (N/km²)', fontsize=28)

# 美化边框
plt.tight_layout()
plt.grid(False)

# 显示图形
# plt.show()
plt.savefig('G:\/Xu\/画图\/成图\/figure5/house.jpg', dpi = 600)
