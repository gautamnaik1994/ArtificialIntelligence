from utils import *

# `grid` is defined in the test code scope as the following:
# (note: changing the value here will _not_ change the test code)
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    sdict = dict(zip(boxes, values))
    sdict = eliminate(sdict)
    # display(sdict)
    sdict = only_choice(sdict)
    return sdict

#print(dict(zip(boxes, grid)))


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        # print("box " + unit)
        for digit in '123456789':
            hit = 0
            b = ''
            for box in unit:
                if digit in values[box]:
                    # print("digit : "+digit + ", box " + box + ", value " + values[box])
                    hit = hit+1
                    b = box
            if(hit == 1):
                values[b] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values);
        # Your code here: Use the Only Choice Strategy
        values=only_choice(values);
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    sdict= reduce_puzzle(values)
    print("=================================================================")
    print("============================Inside===============================")
    print("=================================================================")
    display(sdict)
    solved_values = [box for box in sdict.keys() if len(values[box]) == 1]
    int_length = 2
    if len(solved_values) == 81 :
        return values
    else:
        found_value=''
        found_key=''
        for key,value in sdict.items():
            if(len(value)==int_length):
                found_value=value
                found_key=key
                break
        
        for val in found_value:
            newSu = sdict.copy()
            newSu[found_key]=val
            attempt = search(newSu)
            if attempt:
                return attempt
    
# print(unitlist);
print("=================================================================")
print("==============================Main===============================")
print("=================================================================")
display(search(grid_values(grid2)))
