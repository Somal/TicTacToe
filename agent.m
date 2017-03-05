function [i, j, k] = playTTTT(board, player)
% convert to 1d array for processing
convertedarray = reshape(board, 1, 64)
% preparation
commandStr = 'python 3d/game3D.py ';
for i=1:length(convertedarray)
    commandStr = [commandStr,int2str(convertedarray(i)),' '];
end
commandStr = [commandStr, int2str(player)];
% transfer to python for processing
system(commandStr);
end