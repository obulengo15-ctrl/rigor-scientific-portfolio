% ==============================================================================
% Project: Spatial Interpolation of Gridded Climate Data
% Author: Rigor Scientific Solutions
% Objective: Demonstrate clean, vectorized MATLAB code for matrix operations 
%            and spatial data visualization.
% ==============================================================================

clear; clc; close all;

% 1. Generate Mock Gridded Data (e.g., ERA5 temperature over East Africa)
lon = 25:0.5:45;  % Longitude
lat = -10:0.5:10; % Latitude
[LON, LAT] = meshgrid(lon, lat);

% Simulate a spatial temperature field with a gradient
Z = 30 - 0.5*(LAT - 0) - 0.2*(LON - 35) + randn(size(LAT))*1.5; 

% 2. Introduce Missing Data (Simulating cloud cover/sensor gaps)
Z(10:15, 20:25) = NaN;

% 3. Spatial Interpolation (Griddata)
% Create scattered points from the valid data to interpolate back to the grid
valid_idx = ~isnan(Z);
Xq = LON(valid_idx);
Yq = LAT(valid_idx);
Vq = Z(valid_idx);

% Interpolate using 'natural' neighbor method to fill NaNs
Z_interpolated = griddata(Xq, Yq, Vq, LON, LAT, 'natural');

% 4. Publication-Ready Visualization
figure('Position', [100, 100, 800, 600]);
contourf(LON, LAT, Z_interpolated, 20, 'LineStyle', 'none');
colormap(jet);
colorbar('Label', 'Temperature (°C)', 'FontSize', 12);
hold on;
plot(Xq, Yq, 'k.', 'MarkerSize', 4); % Plot original station points
hold off;

title('Spatial Interpolation of Gridded Temperature Data', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Longitude (°E)', 'FontSize', 12);
ylabel('Latitude (°N)', 'FontSize', 12);
print('spatial_interpolation_output', '-dtiff', '-r300'); % Export 300 DPI TIFF