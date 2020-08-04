set terminal png size 1000, 700
set output 'surface_cells.png'

set pm3d
set grid
set logscale zcb

set xlabel 'Triangle Size' rotate parallel
set ylabel 'Sample Size (no. of cells)' rotate parallel
set zlabel 'Occurrences' rotate parallel
set title 'Triangle Size Distribution for Increasing Sample Sizes'

splot 'gnuplot/surface_cells.dat' pt 0
