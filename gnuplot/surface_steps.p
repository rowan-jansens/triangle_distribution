
set terminal png size 1000, 700
set output 'surface_steps.png'

set pm3d
set grid
set logscale zcb

set xlabel 'Triangle Size' rotate parallel
set ylabel 'Sample Size (no. of steps)' rotate parallel
set zlabel 'Occurrences' rotate parallel
set title 'Triangle Size Distribution for Increasing Sample Sizes'

splot 'gnuplot/surface_steps.dat' pt 0
