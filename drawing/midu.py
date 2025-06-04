import numpy as np
import scipy.io
import rasterio
from rasterio.transform import Affine

# 定义分辨率和地理坐标
reso = 0.01
lat = np.arange(20.211691 + reso / 2, 31.181691 - reso / 2 + reso, reso)
lon = np.arange(109.655529 + reso / 2, 122.835529 - reso / 2 + reso, reso)

# 读取 .mat 文件
mat_file = r'D:\density\density.mat'  # 替换为你的 .mat 文件路径
try:
    mat_data = scipy.io.loadmat(mat_file)
    # 假设 .mat 文件中包含一个名为 'data' 的数组
    data = mat_data['density']
except KeyError:
    print("错误: .mat 文件中未找到 'data' 数组。")
except FileNotFoundError:
    print("错误: 文件未找到。")
except Exception as e:
    print(f"错误: 发生了一个未知错误: {e}")
else:
    data = np.rot90(data)
    # 创建仿射变换
    transform = Affine.translation(lon[0] - reso / 2, lat[-1] + reso / 2) * Affine.scale(reso, -reso)

    # 定义地理参考信息
    crs = rasterio.crs.CRS.from_epsg(4326)  # WGS84

    # 保存为 GeoTIFF 文件
    output_file = r'D:\density\density.tif'
    with rasterio.open(
        output_file,
        'w',
        driver='GTiff',
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(data, 1)

    print(f"GeoTIFF 文件已保存为 {output_file}")