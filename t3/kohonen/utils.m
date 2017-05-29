% function [y, net] = kohonen(csv_data, num_classes, train_percent)
function [y, net] = kohonen(params)
    % ---- Parameter evaluation ----
    csv_data = params.csv_data;
    num_classes = params.num_classes;
    train_percent = params.train_percent;
    if (isfield(params, 'dimensions'))
        dimensions = params.dimensions;
    else
        dimensions = [10 10];
    end

    % ---- Dataset shuffling ----
    dimensions = size(csv_data);
    num_values = dimensions(1); % one parameter value per row
    num_samples = dimensions(2); % one sample per column
    csv_data = csv_data(:,randperm(num_samples)); % shuffles the samples

    % ------ Training/test set construction ------
    training_boundary = int64(num_samples * train_percent);
    training_set = csv_data(:,1:training_boundary);

    test_set = csv_data(:,(training_boundary + 1):end);
    test_set((num_values + 1 - num_classes):end,:) = 0;

    % ------ Self-Organizing Map construction ------
    net = selforgmap(dimensions, 100, 3, 'gridtop');

    % Train the Network
    [net,tr] = train(net,training_set);

    % Test the Network
    y = net(test_set);
end
