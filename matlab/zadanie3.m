figure('Position', [100, 100, 1000, 800], 'Color', 'w');

patternV = repmat(linspace(0, 255, 100)', 1, 100);
patternH = repmat(linspace(0, 255, 100), 100, 1);
x = linspace(0, 255, 100);
y = linspace(0, 255, 100);
[X, Y] = meshgrid(x, y);
patternD  = (X + Y) / 2;
patternD2 = (X - Y) / 2 + 127.5;

subplot(2, 2, 1);
imagesc(patternV);
colormap(gca, parula);
cb = colorbar; cb.TickLabels = {'0','50','100','150','200','250'};
title('colormap = parula', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');
axis image;

subplot(2, 2, 2);
imagesc(patternH);
colormap(gca, cool);
cb = colorbar; cb.TickLabels = {'0','50','100','150','200','250'};
title('colormap = cool', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');
axis image;

subplot(2, 2, 3);
imagesc(patternD);
colormap(gca, gray);
cb = colorbar; cb.TickLabels = {'0','50','100','150','200','250'};
title('colormap = gray', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');
axis image;

subplot(2, 2, 4);
imagesc(patternD2);
colormap(gca, hsv);
cb = colorbar; cb.TickLabels = {'0','50','100','150','200','250'};
title('colormap = hsv', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');
axis image;

sgtitle('Паттерны в RGB', ...
        'FontSize', 11, 'FontWeight', 'bold');



% 2 задание

img = imread('image.jpg');

R = img(:, :, 1);
G = img(:, :, 2);
B = img(:, :, 3);

img_R = img; img_R(:, :, 2) = 0; img_R(:, :, 3) = 0;
img_G = img; img_G(:, :, 1) = 0; img_G(:, :, 3) = 0;
img_B = img; img_B(:, :, 1) = 0; img_B(:, :, 2) = 0;

figure('Position', [100, 100, 1200, 800], 'Color', 'w');

subplot(2, 2, 1);
imshow(img_R);
title('Красный канал', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');

subplot(2, 2, 2);
imshow(img_G);
title('Зелёный канал', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');

subplot(2, 2, 3);
imshow(img_B);
title('Синий канал', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');

subplot(2, 2, 4);
imshow(img);
title('RGB изображение', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');

sgtitle('Каналы изображения', 'FontSize', 14, 'FontWeight', 'bold');


% 3 задание

figure('Position', [100, 100, 1000, 800], 'Color', 'w');

subplot(2, 1, 1);
imshow(img);
title('JPEG картинка', 'FontWeight', 'bold');
xlabel('Ширина, px'); ylabel('Высота, px');

subplot(2, 1, 2);
hold on;

histogram(R(:), 256, 'FaceColor', 'r', 'EdgeColor', 'none', 'FaceAlpha', 0.5);
histogram(G(:), 256, 'FaceColor', 'g', 'EdgeColor', 'none', 'FaceAlpha', 0.5);
histogram(B(:), 256, 'FaceColor', 'b', 'EdgeColor', 'none', 'FaceAlpha', 0.5);

brightness = mean(img, 3);
histogram(brightness(:), 256, 'FaceColor', 'w', 'EdgeColor', 'k', 'FaceAlpha', 0.3);

xlabel('Яркость пикселя');
ylabel('Количество пикселей');
title('Поканальная гистограмма яркости', 'FontWeight', 'bold');
legend('red', 'green', 'blue', 'brightness');
grid on;
hold off;

%4 задание

img_gaussian = imnoise(img, 'gaussian', 0, 0.01);
img_sp = imnoise(img, 'salt & pepper', 0.05);

img_gaussian_filtered = medfilt2d_custom(img_gaussian, 3);
img_sp_filtered = medfilt2d_custom(img_sp, 3);

figure('Position', [100, 100, 1200, 900], 'Color', 'w');

subplot(3, 2, 1);
imshow(img);
title('Исходное изображение', 'FontWeight', 'bold');

subplot(3, 2, 2);
imshow(img_gaussian);
title('Гауссов шум', 'FontWeight', 'bold');

subplot(3, 2, 3);
imshow(img_gaussian_filtered);
title('Медианный фильтр (гауссов)', 'FontWeight', 'bold');

subplot(3, 2, 4);
imshow(img_sp);
title('Шум "соль и перец"', 'FontWeight', 'bold');

subplot(3, 2, 5);
imshow(img_sp_filtered);
title('Медианный фильтр (соль и перец)', 'FontWeight', 'bold');


%5 задание


windows = [3, 5, 7, 9];
mse_gaussian = zeros(size(windows));
mse_sp = zeros(size(windows));

for k = 1:length(windows)
    w = windows(k);
    filtered_gaussian = medfilt2d_custom(img_gaussian, w);
    filtered_sp = medfilt2d_custom(img_sp, w);
    mse_gaussian(k) = mean((double(img(:)) - double(filtered_gaussian(:))).^2);
    mse_sp(k) = mean((double(img(:)) - double(filtered_sp(:))).^2);
end
fprintf('\n=== СКО для разных окон ===\n');
fprintf('Окно | Гауссов шум | Соль и перец\n');
fprintf('-----|-------------|-------------\n');
for k = 1:length(windows)
    fprintf('%4d | %11.2f | %11.2f\n', windows(k), mse_gaussian(k), mse_sp(k));
end

figure('Color', 'w');
plot(windows, mse_gaussian, 'b-o', 'LineWidth', 2, 'MarkerSize', 8);
hold on;
plot(windows, mse_sp, 'r-s', 'LineWidth', 2, 'MarkerSize', 8);
xlabel('Размер окна');
ylabel('СКО (MSE)');
title('Зависимость СКО от размера окна', 'FontWeight', 'bold');
legend('Гауссов шум', 'Соль и перец');
grid on;


%функция

function output = medfilt2d_custom(input, window)
    half = floor(window / 2);

    if size(input, 3) == 3
        output = zeros(size(input), 'uint8');
        for ch = 1:3
            output(:, :, ch) = medfilt2d_custom(input(:, :, ch), window);
        end
        return;
    end

    input = double(input);
    [rows, cols] = size(input);
    padded = padarray(input, [half, half], 'replicate');
    output = zeros(rows, cols);

    for i = 1:rows
        for j = 1:cols
            window_data = padded(i:i+window-1, j:j+window-1);
            output(i, j) = median(window_data(:));
        end
    end

    output = uint8(output);
end

