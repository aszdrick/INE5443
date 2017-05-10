clear all

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
