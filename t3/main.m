clear all
load workspace.mat

num_datasets = 10;
dimensions = size(x0);
num_rows = dimensions(1,1);
num_columns = dimensions(1,2);

X = zeros(num_datasets, num_rows * num_columns);
X(1,:) = normalize_dataset(x0);
X(2,:) = normalize_dataset(x1);
X(3,:) = normalize_dataset(x2);
X(4,:) = normalize_dataset(x3);
X(5,:) = normalize_dataset(x4);
X(6,:) = normalize_dataset(x5);
X(7,:) = normalize_dataset(x6);
X(8,:) = normalize_dataset(x7);
X(9,:) = normalize_dataset(x8);
X(10,:) = normalize_dataset(x9);

num_classes = 10
Y = zeros(num_datasets, num_classes)
for i = 1 : num_datasets
    Y(i, i) = 1;
end

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
