clear all
load exdata.mat

% displayData(X, 20);

normalized = zeros(10, length(y));
for i = 1 : length(y)
    for j = 1 : 10
        normalized(j, i) = 0;
    end
    normalized(y(i), i) = 1;
end

net = newff(minmax(X), normalized,[40 10],{'logsig', 'logsig'},'traingdx');

net.trainParam.epochs = 5000;
net.trainParam.goal = 0.001;
net.trainParam.max_fail = 50;


%net.divideParam.trainRatio = 1.0; %0.85;
%net.divideParam.valRatio   = 0.0; %0.10;
%net.divideParam.testRatio  = 0.0; %0.05;

%net.trainParam.showWindow = 0;

net = train(net, X, normalized);
Y = sim(net, X);

%plotconfusion(normalized, Y);
z = net(X);
tind = vec2ind(normalized);
yind = vec2ind(z);
percentErrors = sum(tind ~= yind)/numel(tind);
percentCorrect = 1 - percentErrors;
fprintf('Percent correct: %.2f%%\n', percentCorrect * 100);
