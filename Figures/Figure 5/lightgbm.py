from sklearn.inspection import plot_partial_dependence
from scipy.stats import pearsonr
from math import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
# import xarray as xr
import scipy.io as sio
import os
import numpy as np
import pandas as pd
import warnings
import lightgbm as lgb
import random as python_random
from sklearn.model_selection import train_test_split
# import datetime
import shap
from scipy.stats import linregress

os.environ["CUDA_VISIBLE_DEVICES"] = " "
warnings.filterwarnings("ignore")

np.random.seed(1)
python_random.seed(1)


params = {
    'boosting_type': 'gbdt',
    'num_leaves': 400,
    'learning_rate': 0.02,
    'use_missing':'false',
    'verbose': 1
}

x_data = sio.loadmat('H:/目标检测绘图/figure62/figure6/x.mat')
y_data = sio.loadmat('H:/目标检测绘图/figure62/figure6/y.mat')
x_all = x_data['x']
sm = y_data['y']

x_all = x_all.reshape(x_all.shape[0] * x_all.shape[1], x_all.shape[2])
sm = sm.reshape(sm.shape[0] * sm.shape[1], 1)
index = ~np.isnan(sm)
non_nan_rows = ~np.isnan(x_all).any(axis=1)
x_all = x_all[non_nan_rows]
sm = sm[non_nan_rows]

x_train, x_test, y_train, y_test = train_test_split(x_all, sm, test_size=0.3, random_state=1)

model = lgb.LGBMRegressor(**params, n_estimators=500)
model.fit(x_train, y_train.ravel())

s = np.zeros(( y_test.shape[0], 1)) * np.nan
index_nan = np.isnan(x_test[:, 1]) | np.isnan(x_test[:, -1])
s[:, 0] = model.predict(x_test)

correlation_matrix = np.corrcoef(s[:,0], y_test[:,0])
correlation_coefficient = correlation_matrix[0, 1]  # 因为是两个变量，所以是矩阵的[0,1]位置

print("相关系数:", correlation_coefficient)


##lightgbm特征重要性
# feature_importance = model.feature_importances_
# booster = model.booster_
# feature_importance = booster.feature_importance(importance_type='gain')
# np.savetxt('feature_importance.csv', feature_importance, delimiter=',', fmt='%d')
# # 将特征重要性与特征名对应
# feature_names =['pop', 'gdp', 'per_gdp', 'dem', 'geomor', 'land', 'rsei', 'ndvi', 'npp', 'tem'
#                                          , 'preci', 'river', 'coastline', 'scenery_distance', 'city_index', 'province_index'
#                                          , 'lat_matrix', 'lon_matrix', 'policy', 'house']
# sorted_indices = feature_importance.argsort()
# sorted_feature_names = [feature_names[i] for i in sorted_indices]
# sorted_importance = feature_importance[sorted_indices]
#
# # 绘制特征重要性图
# plt.figure(figsize=(8, 6))
# plt.barh(sorted_feature_names, sorted_importance)
# plt.xlabel('Feature Importance')
# plt.ylabel('Features')
# plt.title('LightGBM Feature Importance')
# plt.show()
# print()


###散点拟合图
# y = s[:,0]
# x = y_test[:,0]
# df = pd.DataFrame({
#     'Detected gravesite density': x,
#     'Predicted gravesite density': y
# })
#
# # df.to_csv('pred_true.csv', index=False)
#
# slope, intercept, r_value, p_value, std_err = linregress(x, y)
# line = slope * x + intercept
# r_squared = r_value ** 2
# # 设置图片清晰度
# plt.rcParams['figure.dpi'] = 300
# plt.rcParams['font.family'] = 'Times New Roman'
# # 绘制散点图
# plt.scatter(x, y, label='Testing data samples')
#
# # 绘制拟合直线
# plt.plot(x, line, color='red', label=f'Fit line: y = {slope:.3f}x + {intercept:.3f}')
#
# # 添加图标题和轴标签
#
# plt.xlabel('Detected gravesite density')
# plt.ylabel('Predicted gravesite density')
# plt.text(0.05, 0.9, f'$R^2$ = {r_squared:.3f}', transform=plt.gca().transAxes)
# plt.text(0.05, 0.85, f'$P$ = {p_value:.3f}', transform=plt.gca().transAxes)
# # 显示图例
# plt.legend()
# # plt.savefig('H:/目标检测绘图/figure62/figure6/figure/fit.png', dpi=300, bbox_inches='tight')
# # 显示图形
# plt.show()

# ###计算SHAP，特征重要性
# explainer = shap.TreeExplainer(model)
# # 以numpy数组的形式输出SHAP值
#
# shap_values = explainer.shap_values(x_train)
# abs_arr = np.abs(shap_values)
# abs_means = np.mean(abs_arr, axis=0)
# df_2d = pd.DataFrame([abs_means], columns=['pop', 'gdp', 'per_gdp', 'dem', 'geomor', 'land', 'rsei', 'ndvi', 'npp', 'tem'
#                                          , 'preci', 'river', 'coastline', 'scenery_distance', 'city_index', 'province_index'
#                                          , 'lat_matrix', 'lon_matrix', 'policy', 'house'])
# df_2d.to_csv('mean_shap_xtrain_nonan.csv', index=False)
# # shap.summary_plot(shap_values, x1000, plot_type="bar")
# print('a')

###计算部分依赖关系（PDP）偏相关
# features = [17, 12, 2, 9, 6, 3]   #选择特征
#
# # non_nan_rows = ~np.isnan(x_train).any(axis=1)
# # new_arr = x_train[non_nan_rows]
#
# display = plot_partial_dependence(model, x_train, features, grid_resolution=50)
# partial_data = display.pd_results
#
# excel_file = pd.ExcelWriter('H:\\目标检测绘图\\figure62\\figure6\\pdp_nonan_gain50.xlsx')
#
# for i, result in enumerate(display.pd_results):
#     values = result['values'][0]
#     average = result['average'].flatten()
#
#     # 创建 DataFrame
#     df = pd.DataFrame({
#         f'feature_{features[i]}': values,
#         'y': average
#     })
#
#     # 将 DataFrame 写入 Excel 文件的不同 sheet
#     sheet_name = f'feature_{features[i]}'
#     df.to_excel(excel_file, sheet_name=sheet_name, index=False)
#     print(f'部分依赖结果已保存到 Excel 文件的 {sheet_name} sheet 中')
#
# # 保存 Excel 文件
# excel_file.save()
# print()

