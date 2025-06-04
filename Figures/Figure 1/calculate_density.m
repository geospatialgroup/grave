
% calculate_density
clear all
clc

file = 'E:\青山白化\data\shapefile\study_area.tif';
data = imread(file);
data = data';
data = double( data );
data = data(:, end:-1:1);
index_studyarea = find(data<=3);


area = importdata( 'E:\青山白化\data\area.mat');
density = nan( size(area));
density(index_studyarea) = 0;


reso=0.01;
lat = 20.211691+reso/2:0.01:31.181691-reso/2;
lon = 109.655529 +reso/2 :0.01:122.835529-reso/2;
lat_matrix = repmat(lat,[length(lon) 1]);
lon_matrix = repmat(lon',[1 length(lat)]);

file = 'E:\青山白化\data\福建省\detect\detect.shp';
S = shaperead(file);

for j=1:size(S,1)
    xv  = S(j).X;
    yv = S(j).Y;
    index_lon = round(( xv - lon(1) ) / reso) + 1;
    index_lat = round(( yv - lat(1) ) / reso) + 1;
    if index_lon<1 || index_lon>length(lon)
        continue;
    end
    if index_lat<1 || index_lat>length(lat)
        continue;
    end
    t = density(index_lon, index_lat);
    if t==0
        t = 1;
    else
        t = t+1;
    end
    density(index_lon, index_lat) = t;
    
end
    
%%
file = 'E:\青山白化\data\浙江省\detect\detect.shp';
S = shaperead(file);

for j=1:size(S,1)
    xv  = S(j).X;
    yv = S(j).Y;
    index_lon = round(( xv - lon(1) ) / reso) + 1;
    index_lat = round(( yv - lat(1) ) / reso) + 1;
    if index_lon<1 || index_lon>length(lon)
        continue;
    end
    if index_lat<1 || index_lat>length(lat)
        continue;
    end
    t = density(index_lon, index_lat);
    if t==0
        t = 1;
    else
        t = t+1;
    end
    density(index_lon, index_lat) = t;
    
end
%%
file = 'E:\青山白化\data\广东省\detect\detect.shp';
S = shaperead(file);

for j=1:size(S,1)
    xv  = S(j).X;
    yv = S(j).Y;
    index_lon = round(( xv - lon(1) ) / reso) + 1;
    index_lat = round(( yv - lat(1) ) / reso) + 1;
    if index_lon<1 || index_lon>length(lon)
        continue;
    end
    if index_lat<1 || index_lat>length(lat)
        continue;
    end
    t = density(index_lon, index_lat);
    if t==0
        t = 1;
    else
        t = t+1;
    end
    density(index_lon, index_lat) = t;
    
end

save( 'E:\青山白化\data\number.mat','density');
density = density ./area; % number / km^2

save( 'E:\青山白化\data\density.mat','density');


file = 'E:\青山白化\data\shapefile\study_area.tif';
data = imread(file);
data = data';
data = double( data );
data = data(:, end:-1:1);
index = find(data==1);% 
density_zhejiang = nan( size(density));
density_zhejiang(index) = density(index);


index = find(data==2);% 
density_fujian = nan( size(density));
density_fujian(index) = density(index);

index = find(data==3);% 
density_guangdong = nan( size(density));
density_guangdong(index) = density(index);

save( 'E:\青山白化\data\density_zhejiang.mat','density_zhejiang');
save( 'E:\青山白化\data\density_fujian.mat','density_fujian');
save( 'E:\青山白化\data\density_guangdong.mat','density_guangdong');


%%

reso=0.01;
lat = 20.211691+reso/2:0.01:31.181691-reso/2;
lon = 109.655529 +reso/2 :0.01:122.835529-reso/2;
lat_matrix = repmat(lat,[length(lon) 1]);
lon_matrix = repmat(lon',[1 length(lat)]);

data = density_zhejiang';
data = data(end:-1:1,:);
% lat = linspace(lat(1), lat(end), 100);
% lon = linspace(-110, -90, 200);

% 定义地理变换（仿射变换参数）
dx = (lon(end) - lon(1)) / (size(data, 2) - 1);
dy = (lat(end) - lat(1)) / (size(data, 1) - 1);
xmin = lon(1) - dx/2;
ymax = lat(end) + dy/2;
affine = [dx 0 xmin; 0 -dy ymax];

%  clear option
 option.GTModelTypeGeoKey = 2;
 option.ModelPixelScaleTag = [0.010000000000000;0.010000000000000;0];
 option.ModelTiepointTag = [0;0;0;109.6605;31.1767;0];
 option.GeographicTypeGeoKey = 4030;
 option.GeogGeodeticDatumGeoKey = 6326;
%  option.GTCitationGeoKey = 'UTM Zone 16N NAD27"';
%  option.GeogCitationGeoKey = 'Clarke, 1866 by Default';
 geotiffwrite('E:\青山白化\data\density_zhejiang.tif',[],data,32,option);

% 写入 GeoTIFF
% geotiffwrite('E:\青山白化\data\温度降水湿度\tem.tif', data, affine, 'CoordRefSysCode', 4326); % 4326 = WGS84



data = density_fujian';
data = data(end:-1:1,:);
geotiffwrite('E:\青山白化\data\density_fujian.tif',[],data,32,option);


data = density_guangdong';
data = data(end:-1:1,:);
geotiffwrite('E:\青山白化\data\density_guangdong.tif',[],data,32,option);