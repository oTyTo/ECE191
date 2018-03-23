%matrix analysis
%% load images
load('origin.mat');
load('scaled.mat');
%convert opencv BGR to RGB
temp = origin(:,:,3);
origin(:,:,3) = origin(:,:,1);
origin(:,:,1) = temp;
temp = scaled(:,:,3);
scaled(:,:,3) = scaled(:,:,1);
scaled(:,:,1) = temp;
%% show RGB image
figure()
imshow(origin);
figure()
imshow(scaled);
%% show channels
for i = 1:1:size(origin,3)
    figure()
    imshow(origin(:,:,i));
    figure()
    imshow(scaled(:,:,i));
    figure()
    imshow(scaled(:,:,i),[]);
end