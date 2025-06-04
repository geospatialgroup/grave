import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Arial
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 18  # 基础字体大小

# 读取Excel文件
df = pd.read_excel(r"G:\目标检测\结果\PR_curve_finaresult.xlsx")

# 提取数据
recall = df["recall"].values
precision = df["precision"].values
threshold_recall = 0.821
threshold_precision = 0.821

# 创建图表
plt.figure(figsize=(10, 7))

# 绘制PR曲线
plt.plot(recall, precision,
         label="PR Curve",
         color="blue",
         linewidth=3,
         linestyle="--")

# 标记阈值点
plt.scatter(threshold_recall, threshold_precision,
            color="blue",
            marker="x",
            s=250,
            linewidth=8,
            zorder=10)  # 确保标记在最上层

# 设置坐标轴标签和标题
plt.xlabel("Recall", fontweight='bold')
plt.ylabel("Precision", fontweight='bold')
plt.title("Precision-Recall Curve", fontweight='bold', pad=20)

# 设置坐标轴范围和刻度
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.tick_params(axis='both', which='major', labelsize=16)

# 设置图例
legend = plt.legend(
    loc="lower center",
    handlelength=2.5,
    fontsize=16,
    borderpad=0.8,
    framealpha=1  # 不透明背景
)
legend.get_texts()[0].set_text("Thresh=0.53, Prec=0.821, Rec=0.821")
legend.set_bbox_to_anchor((0.5, 0.02))

# 优化布局
plt.tight_layout()

# 保存图像（600dpi，适合出版物质量）
plt.savefig(
    './pr_curve.png',
    dpi=600,
    bbox_inches='tight',
    facecolor='white'  # 确保背景是白色
)

# 显示图表
plt.show()