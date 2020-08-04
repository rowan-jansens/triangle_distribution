#!/bin/bash

gnuplot gnuplot/simple_distribution.p
gnuplot gnuplot/surface_steps.p
gnuplot gnuplot/surface_cells.p
xdg-open simple_distribution.png
xdg-open surface_steps.png
xdg-open surface_cells.png


