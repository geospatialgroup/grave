# import xarray as xr
import os
import numpy as np
import hdf5storage
# import pandas as pd
import warnings
import lightgbm as lgb
import random as python_random
from sklearn.model_selection import train_test_split
# import datetime

os.environ["CUDA_VISIBLE_DEVICES"] = " "
warnings.filterwarnings("ignore")

np.random.seed(1)
python_random.seed(1)

params = {
    'task': 'train',
    'boosting': 'gbdt',
    'objective': 'regression',
    'use_missing':'false',
    'num_leaves': 400,
    'learning_rate': 0.02,
    'metric': {'l2'},
    'verbose': 1
}

# for index_lead in range(0,14):
sm = hdf5storage.loadmat('E:/青山白化/data/y.mat')
sm = sm['y']
#
x_all = hdf5storage.loadmat('E:/青山白化/data/x.mat')
x_all = x_all['x']

x_all = x_all.reshape(x_all.shape[0] * x_all.shape[1], x_all.shape[2])
sm = sm.reshape(sm.shape[0] * sm.shape[1], 1)
index = ~np.isnan(sm)
sm = sm[index[:,0],:]
x_all = x_all[index[:,0],:]

x_train, x_test, y_train, y_test = train_test_split(x_all, sm, test_size=0.3, random_state=1)
lgb_train = lgb.Dataset(x_train, y_train)
lgb_eval = lgb.Dataset(x_test, y_test, reference=lgb_train)
# model = LGBMRegressor()

evals_result = {}
model = lgb.train(params,
                  train_set=lgb_train,
                  valid_sets=[lgb_train, lgb_eval],
                  valid_names=['train','eval'],
callbacks = [lgb.record_evaluation(evals_result)],
                  num_boost_round=500)

print(evals_result)
tn_ = np.array(evals_result['train']['l2'])
tt_ = np.array(evals_result['eval']['l2'])

# model.fit(x_tn, y_tn)
s = np.zeros(( y_test.shape[0], 1)) * np.nan
index_nan = np.isnan(x_test[:, 1]) | np.isnan(x_test[:, -1])
s[:, 0] = model.predict(x_test)

correlation_matrix = np.corrcoef(s[:,0], y_test[:,0])
correlation_coefficient = correlation_matrix[0, 1]  # 因为是两个变量，所以是矩阵的[0,1]位置

print("相关系数:", correlation_coefficient)




