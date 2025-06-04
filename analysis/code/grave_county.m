
%% rf_grave
close all
clear all
clc

tem = importdata( 'E:\tem_county.mat');
preci = importdata( 'E:\preci_county.mat');


dem = xlsread( 'E:\dem.dbf',1,'a2:d299');
dem = dem(:,[1 4]);
dem_new = nan(298,1);
dem_new( dem(:,1)) = dem(:,2);
dem = dem_new;

% coastline.dbf
coastline = xlsread( 'E:\coastline.dbf',1,'a2:d299');
coastline = coastline(:,[1 4]);
coastline_new = nan(298,1);
coastline_new( coastline(:,1)) = coastline(:,2);
coastline = coastline_new;


gdp = xlsread( 'E:\gdp.dbf',1,'a2:d299');
gdp = gdp(:,[1 4]);
gdp_new = nan(298,1);
gdp_new( gdp(:,1)) = gdp(:,2);
gdp = gdp_new;


ndvi = xlsread( 'E:\ndvi.dbf',1,'a2:d299');
ndvi = ndvi(:,[1 4]);
ndvi_new = nan(298,1);
ndvi_new( ndvi(:,1)) = ndvi(:,2);
ndvi = ndvi_new;


npp = xlsread( 'E:\npp.dbf',1,'a2:d299');
npp = npp(:,[1 4]);
npp_new = nan(298,1);
npp_new( npp(:,1)) = npp(:,2);
npp = npp_new;


pop = xlsread( 'E:\pop.dbf',1,'a2:d299');
pop = pop(:,[1 4]);
pop_new = nan(298,1);
pop_new( pop(:,1)) = pop(:,2);
pop = pop_new;


river = xlsread( 'E:\river.dbf',1,'a2:d299');
river = river(:,[1 4]);
river_new = nan(298,1);
river_new( river(:,1)) = river(:,2);
river = river_new;


house = xlsread( 'E:\house.dbf',1,'a2:d299');
house = house(:,[1 4]);
house_new = nan(298,1);
house_new( house(:,1)) = house(:,2);
house = house_new;


scenery = xlsread( 'E:\scenery.dbf',1,'a2:d299');
scenery = scenery(:,[1 4]);
scenery_new = nan(298,1);
scenery_new( scenery(:,1)) = scenery(:,2);
scenery = scenery_new;

rsei = xlsread( 'E:\rsei.dbf',1,'a2:d299');
rsei = rsei(:,[1 4]);
rsei_new = nan(298,1);
rsei_new( rsei(:,1)) = rsei(:,2);
rsei = rsei_new;

area = xlsread( 'E:\city_county_Project.dbf',1,'d2:d299');

y = xlsread( 'E:\city_county_spatialjoin.dbf',1,'a2:a299');
y_density = y./area;

per_gdp = gdp ./ pop;
pop_density = pop./area;

% policy = xlsread( 'E:\青山白化\data\政策\city.xlsx',1,'e2:e58');

x = cat(2, area, pop_density,  per_gdp, dem, rsei, ndvi, npp, tem,...
    preci, river, coastline, scenery, house);

% remove_index = [26 49:51 55 57 58 59 62 63 76 77 79 83 87 92 110 112 116:118 141 142 177 179 198:200 205 219 222 223 228 229 247 248 278 281 320:322 324 326 327 332 333 335];

% y(remove_index) = [];
% y_density(remove_index) = [];
% x(remove_index,:) = [];
% coastline(remove_index) = [];
% dem( remove_index) = [];
% gdp( remove_index) = [];
% per_gdp( remove_index) = [];
% pop( remove_index) = [];
% pop_density( remove_index) = [];
% rsei( remove_index) = [];

index = find( ~isnan(y_density) & ~isnan(x(:,7)) & ~isnan(x(:,8)) & ~isnan(x(:,12)) );
% [b,bint,r,rint,stats] = regress( y_density(index,:), [coastline(index) ones( length(index),1)] );
% stats
% 
% 
% [b,bint,r,rint,stats] = regress( y_density(index,:), [dem(index) ones( length(index),1)] );
% stats
% 
% [b,bint,r,rint,stats] = regress( y_density(index,:), [per_gdp(index) ones( length(index),1)] );
% stats
% 
% [b,bint,r,rint,stats] = regress( y_density(index,:), [pop_density(index) ones( length(index),1)] );
% stats

s = [];
b_all = [];
bint_all = [];
for i=1:size(x,2)
    [b,bint,r,rint,stats] = regress( y_density(index,:), [x(index,i) ones( length(index),1)] );
    s = [s;stats];
    b_all = [b_all; [b(1) b(2)]];
    bint_all = [bint_all; [bint(1,1) bint(1,2)]];
end
b_all
s

names = {'area', 'pop_density', 'per_gdp', 'dem', 'rsei', 'ndvi', 'npp', 'tem',...
    'preci', 'river', 'coastline', 'scenery', 'house'};
index = find(s(:,3)<0.01);
names(index)
% [b,stats] = robustfit([dem(index)], y_density(index,:));
% stats

save( 'E:\x.mat','x');
save( 'E:\y.mat','y');
save( 'E:\y_density.mat','y_density');


save( 'E:\x.txt','x','-ascii');
save( 'E:\y.txt','y','-ascii');
save( 'E:\y_density.txt','y_density','-ascii');

%%
% 
% index = 1:size(x,1);
% index_train = randi( length(index), floor( 0.7*length(index) ), 1);
% index_test = setdiff(  (1:length(index))', index_train );
% 
% rng('default');
% rng(1); % for reproducibility
% 
% x_train = x(index(index_train), :);
% x_test = x(index(index_test), :);
% y_train = y(index(index_train), :);
% y_test = y(index(index_test), :);
%     
% rng('default');
% rng(1); % for reproducibility
% index_nonan = find(~isnan( x_train(:,1)) & ~isnan(x_train(:,2)) & ~isnan(x_train(:,3)) & ~isnan(x_train(:,4)) & ~isnan(y_train));
% Mdl = TreeBagger(50, x_train( index_nonan,:), y_train(index_nonan,:) ,'Method','regression','Surrogate','on',...
%     'NumPredictorsToSample','all', 'MinLeafSize', 5, 'OOBPredictorImportance','on');
% y_pre = predict(Mdl, x_test );
% impCART = Mdl.OOBPermutedPredictorDeltaError;% predictor importance
% %     figure;plot(y_pre);hold on;plot(y_train)
% impCART
% figure
% bar(impCART)
% index_nan = find(isnan(x_test(:,end)) | isnan(x_test(:,1)) | isnan(x_test(:,2)) | isnan(x_test(:,3)));
% y_pre( index_nan) = nan;
% 
% index_nonan = find(~isnan( y_pre) & ~isnan(y_test) );
% t = corrcoef( y_pre(index_nonan), y_test(index_nonan) );
% t