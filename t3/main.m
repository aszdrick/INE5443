clear all
load workspace.mat

% num_datasets = 10;
% dimensions = size(x0);
% num_rows = dimensions(1,1);
% num_columns = dimensions(1,2);
% 
% X = zeros(num_datasets, num_rows * num_columns);
% X(1,:) = normalize_dataset(x0);
% X(2,:) = normalize_dataset(x1);
% X(3,:) = normalize_dataset(x2);
% X(4,:) = normalize_dataset(x3);
% X(5,:) = normalize_dataset(x4);
% X(6,:) = normalize_dataset(x5);
% X(7,:) = normalize_dataset(x6);
% X(8,:) = normalize_dataset(x7);
% X(9,:) = normalize_dataset(x8);
% X(10,:) = normalize_dataset(x9);
% 
% num_classes = 10;
% Y = zeros(num_datasets, num_classes);
% for i = 1 : num_datasets
%     Y(i, i) = 1;
% end

pixels_per_image = 150;
num_classes = 10;
X = zeros(1, pixels_per_image);
Y = zeros(1, num_classes);
index = 1;
for k = 0 : 9
    for l = 0 : 20
        if (l == 0)
            filename = strcat('datasets/', num2str(k), '.png');
        else
            letter = char(96 + l);
            filename = strcat('datasets/', num2str(k), '_', letter, '.png');
        end
        pixels = imread(filename);
        X(index,:) = normalize_dataset(pixels);
        
        Y(index,:) = zeros(1, num_classes);
        if (k == 0)
            class_index = 10;
        else
            class_index = k;
        end
        Y(index,class_index) = 1;
        index = index + 1;
    end
end

X = transpose(X);
Y = transpose(Y);

%file = fopen("0.png", "rt");
%content = fread(file);
%content

function result = normalize_dataset(dataset)
    dimensions = size(dataset);
    num_rows = dimensions(1,1);
    num_columns = dimensions(1,2);
    result = [];
    for i = 0 : (num_rows - 1)
        for j = 0 : (num_columns - 1)
            result(i * num_columns + j + 1) = dataset(i+1,j+1,1);
        end
    end
end
