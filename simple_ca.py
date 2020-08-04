#! /usr/bin/env python3

"""Take an initial row and a cellular automaton rule and run the
automaton for a given number of iterations.  Then look at the 
triangle size distibution"""

import random
import math

def main():
    n_cells = 700
    n_steps = 800
    distribution = {}

    simple_distribution(n_steps, n_cells, distribution)
    surface_steps(n_cells, distribution)
    surface_cells(n_steps, distribution)


def print_distribution(distribution):
    for key, value in sorted(distribution.items()):
         print(key, value)

#a function to generate a datafile for a simple distribution plot
def simple_distribution(n_steps, n_cells, distribution):
    f = open("gnuplot/simple_distribution.dat", "w")
    single_run(n_steps, n_cells, distribution)
    for key, value in sorted(distribution.items()):
         f.write(str(key) + ' ' + str(value) + '\n')
    f.close()

#a function to generate a datafile for a more complex suface plot
#of distribution across different n_steps
def surface_steps(n_cells, distribution):
    s = open("gnuplot/surface_steps.dat", "w")
    for j in range (20):
        n_steps = (j+1) * 50   #increment step size by 50
        single_run(n_steps, n_cells, distribution)
        for key, value in sorted(distribution.items()):
            s.write(str(key) + ' ' + str(n_steps) + ' ' + str(value) + '\n')
        s.write('\n')
        distribution.clear()   #clear the dict for next itteration
    s.close()

#a function to generate a datafile for a more complex suface plot
#of distribution across different n_cells
def surface_cells(n_steps, distribution):
    s = open("gnuplot/surface_cells.dat", "w")
    for j in range (20):
        n_cells = (j+1) * 50   #increment step size by 50
        single_run(n_steps, n_cells, distribution)
        for key, value in sorted(distribution.items()):
            s.write(str(key) + ' ' + str(n_cells) + ' ' + str(value) + '\n')
        s.write('\n')
        distribution.clear()   #clear the dict for next itteration
    s.close()

    
#runs the simple_ca one time
def single_run(n_steps, n_cells, distribution):
    
    row = set_first_row_random(n_cells)
    #row = set_first_row_specific_points(n_cells, [250])
    #row = set_first_row_specific_points(n_cells, [200, 600])
    
    #print_row(row)

    rule = '01101000'           # the basic rule
    #rule = '00011110'           # the famous rule 30
    #rule = '01101110'           # the famous rule 110
    #rule = '10011001'
    
    for i in range(n_steps):
        old_row = row
        row = take_step(rule, row)
        #print_row(row)
        get_distribution(n_cells, old_row, row, distribution)


def take_step(rule, row):
    """a single iteration of the cellular automaton"""
    n_cells = len(row)
    new_row = [0]*n_cells
    for i in range(n_cells):
        neighbors = [row[(i - 1 + n_cells) % n_cells], row[i], row[(i + 1) % n_cells]]
        # new_row[i] = new_cell(neighbors)
        ## NOTE: new_cell_with_rule() is part of the extended code (at
        ## the bottom)
        new_row[i] = new_cell_with_rule(rule, neighbors)
    return new_row

def new_cell(neighbors):
    """looks at the neighborhood of three cells and determine what the
    successor of the central cell should be"""
    ## this simple approach decides on the next cell based on the sum
    ## of the neighbors -- if both neighbors are active we are
    ## overcrowded and we die; if one is active then we come to life;
    ## if none are active we starve and die.
    if neighbors[0] + neighbors[2] == 2: # try [0] and [1] for a different pattern
        new_cell = 0
    elif neighbors[0] + neighbors[2] == 1:
        new_cell = 1
    else:
        new_cell = 0
    return new_cell

def set_first_row_random(n_cells):
    """sets the first row to random values"""
    row = [0]*n_cells
    for i in range(n_cells):
        row[i] = random.randint(0, 1)
    return row

def set_first_row_specific_points(n_cells, active_pts):
    """takes a list of specific cells to be activated in the first row"""
    row = [0]*n_cells
    for pt in active_pts:       # only activate the given cells
        print(pt)
        row[pt] = 1
    return row

def print_row(row):
    """prints a row, represented as a blank if the cell is 0 or a special
    symbol (like a period) if it's 1"""
    on_marker = ' '
    row_str = ''
    for cell in row:
        if cell:
            symbol = on_marker
        else:
            symbol = '0'
        print(symbol, end="")
    print()

#builds a dict with the triangle distibution of a given run
def get_distribution(n_cells, old_row, row, distribution):
    triangle_size = 0
    num_triangles = 0
    
    for i in range(n_cells):
        left = old_row[(i - 1 + n_cells) % n_cells]
        top = old_row[i]
        right = old_row[(i + 1) % n_cells]
        
        #Initiate a new triangle as long as the top 3 neighbors are not also "0"
        #EG: A single "1" in any of the top three neighbors indicate a new tringle
        
        if row[i] == 0 and (left != 0 or top != 0 or right != 0) and triangle_size == 0:
            triangle_size += 1
        
        #Increment the size counter for each additional 0 after a new
        #triangle has been identified
        
        elif row[i] == 0 and triangle_size > 0:
            triangle_size += 1

        #Terminate the triangle counter when a 1 is reached in the row
        #If the triangle size is already in the dictionary, increment the value by 1
        #Else, add the size as a new key in the dict and set the vaule as 1
        #Then reset the size_counter
            
        elif row[i] == 1 and row[(i - 1 + n_cells) % n_cells] == 0 and triangle_size > 0:
            distribution[triangle_size] = distribution.get(triangle_size, 0) + 1
            num_triangles += 1
            triangle_size = 0

## NOTE: new_cell_with_rule() is extended code; you can skip it on a
## first implementation
def new_cell_with_rule(rule, neighbors):
    """Applies a rule encoded as a binary string -- since a neighborhood
    of 3 binary cells can have 8 possible patterns, it's a string of 8
    bits.  You can modify it to be any of the 256 possible strings of
    8 bits.  I provide a couple of examples, and you can try many others."""
    if not rule:
        rule = '01101000'       # the default rule
    rule_index = neighbors[0] + 2*neighbors[1] + 4*neighbors[2]
    cell = int(rule[rule_index])
    return cell

if __name__ == '__main__':


    main()
