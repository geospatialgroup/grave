The code for the result analysis part is written in Matlab tools with a .m suffix.

Among them, the calculate_density.m file is used to calculate the density of graves on each 1km grid; the grave_county.m file is based on the regression method to analyze the linear relationship between the density of graves at the county level and the independent variable; the lgb_.py file is written in python and is used to analyze the nonlinear relationship between the density of graves on the 1km grid and the independent variable.

The software versions used in the experiment are Python 3.12.4 and Matlab R2018a.
The pythons required to run lgb_.py include lightgbm, sklearn, scipy and hdf5storage.
Please replace the absolute data path in the code to ensure that the code runs properly.
