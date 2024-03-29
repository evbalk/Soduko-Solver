import numpy as np
import numpy.ma as ma

record_sheet = open("changes_log2.txt", "w")

# easy
'''puzzle = np.array(
    [(0, 0, 1, 0, 8, 3, 0, 7, 6), (0, 7, 0, 4, 0, 0, 2, 1, 0), (6, 0, 9, 0, 0, 0, 0, 8, 0), (5, 4, 3, 0, 9, 1, 0, 6, 0),
     (2, 0, 0, 8, 5, 0, 7, 0, 9), (0, 0, 8, 6, 3, 0, 0, 4, 5), (9, 5, 0, 0, 7, 0, 0, 0, 1), (3, 0, 0, 2, 0, 5, 4, 0, 0),
     (1, 8, 2, 0, 0, 6, 3, 0, 0)])'''

# hard
puzzle = np.array(
    [(0, 0, 0, 0, 0, 0, 6, 8, 0), (0, 0, 0, 0, 7, 3, 0, 0, 9), (3, 0, 9, 0, 0, 0, 0, 4, 5), (4, 9, 0, 0, 0, 0, 0, 0, 0),
     (8, 0, 3, 0, 5, 0, 9, 0, 2), (0, 0, 0, 0, 0, 0, 0, 3, 6), (9, 6, 0, 0, 0, 0, 3, 0, 8), (7, 0, 0, 6, 8, 0, 0, 0, 0),
     (0, 2, 8, 0, 0, 0, 0, 0, 0)])

'''Check to see if array is square, not 0x0'''
l, w = np.shape(puzzle)
assert l == w, "Puzzle shape is not square"
assert l == 9, "Puzzle is not 9x9"

'''Set range of numbers in puzzle'''
pz_size = 9


# creates 9x9 array where each location holds its box number
def square_boundaries(size):
    loc_arr = np.zeros((size, size))
    sqrt = int(size ** (1 / 2))
    for r in range(size):
        for c in range(size):
            loc_arr[r, c] = c // sqrt + sqrt * (r // sqrt)
    return loc_arr


# returns list of (r,c) that are in the same box as the given r,c
def return_locs_in_box(row, column):
    correspond = square_boundaries(9)  # get 9x9 matrix which contains box layout
    my_box = correspond[row, column]  # get the box for this r,c
    output_list = []
    for r in range(9):
        for c in range(9):
            if correspond[r, c] == my_box:  # run through each r,c (81) and figure out which have the same box value
                output_list.append((r, c))  # append those that share the same box value as tuple(r,c)
    return output_list


print(return_locs_in_box(5, 1))


# clears a number from its corresponding candidates matrix row
def clear_row(number, row, array_to_clear, exceptions=[]):
    for i in range(9):
        if i not in exceptions:
            array_to_clear[number, row, i] = 0


# clears a number from its corresponding candidates matrix column
def clear_column(number, column, array_to_clear, exceptions=[]):
    for i in range(9):
        if i not in exceptions:
            array_to_clear[number, i, column] = 0


# clears a number from its corresponding candidates matrix box
def clear_box(number, row, column, array_to_clear):
    for location in return_locs_in_box(row, column):
        r, c = location
        array_to_clear[number, r, c] = 0


# when a number is solved, have to update puzzle and candidate layers
def update_whole(number, row, column, array_to_update):
    array_to_update[0, row, column] = number
    array_to_update[number, row, column] = 0
    clear_row(number, row, array_to_update)
    clear_column(number, column, array_to_update)
    clear_box(number, row, column, array_to_update)
    master_arr[10] = candidates_count(array_to_update)
    print(number, (row, column))


square_divvy = square_boundaries(pz_size)
# 0 is the actual puzzle, 1-9 are candidate matrices, 10 contains total number of candidates in
master_arr = np.zeros((pz_size + 3, pz_size, pz_size))
master_arr = master_arr.astype(int)
master_arr[0, :, :] = puzzle

# initialize the candidate matrices
for i in range(1, 10):
    master_arr[i, :, :] = i

# remove candidates in spot that have been solved for
for r in range(9):
    for c in range(9):
        if master_arr[0, r, c] != 0:
            master_arr[1:, r, c] = 0

# remove candidates based on interference from solved spots in terms of row and column
for i in range(1, 10):
    for r in range(9):
        if i in master_arr[0, r]:
            clear_row(i, r, master_arr)
    for c in range(9):
        if i in master_arr[0, :, c]:
            clear_column(i, c, master_arr)

# remove illegal candidates on the basis of their box membership
for r in range(9):
    for c in range(9):
        if master_arr[0, r, c] != 0:
            clear_box(master_arr[0, r, c], r, c, master_arr)


# generates an array that stores the number of candidates in each position
def candidates_count(array_to_check):
    output = np.zeros((9, 9))
    count = 0
    for r in range(9):
        for c in range(9):
            for i in range(1, 10):
                if array_to_check[i, r, c] != 0:
                    count += 1
            output[r, c] = count
            count = 0
    return output


master_arr[10, :, :] = candidates_count(master_arr)


# given a row or column, return a list which contains the candidates in each column or row
def get_candidates(type, num, array_to_check):
    output_list = []
    temp = []
    # stupid way
    if type == "row":
        for col in range(9):
            temp = []
            for depth in range(1, 10):
                if array_to_check[depth, num, col] != 0:
                    temp.append(depth)
            output_list.append((col, temp))
    '''if type == "row": #comeback for later
        for j in range(9):
            a = []
            a = ma.masked_equal(array_to_check[:, num, j], 0)
            b = a[~a.mask]
            output_list[j] = b'''
    if type == "col":
        for row in range(9):
            temp = []
            for depth in range(1, 10):
                if array_to_check[depth, row, cum] != 0:
                    temp.append(depth)
            output_list.append((row, temp))
    return output_list


def get_candidates2(array):
    for i in range(1, 10):  # 1-4/9
        for rw in range(9):
            for col in range(9):
                candidates=[]
                if array[0, rw, col] == 0:  # is the specific location not already occupied/solved
                    if i not in array[0, rw, :]:  # checks rows for the number
                        if i not in array[0, :, col]:  # checks each column for the number
                            shared_box = return_locs_in_box(rw, col)
                            in_box = False
                            for entry in shared_box:
                                r1, c1 = entry
                                if array[0, r1, c1] == i:
                                    in_box = True
                            if in_box is False:
                                array[11, rw, col] = i


get_candidates2(master_arr)


# creates a list
def unsolved_list(the_array):
    output_list = []
    for r in range(9):
        for c in range(9):
            if master_arr[10, r, c] != 0:
                output_list.append((r, c))
    return output_list


test = get_candidates("got", 1, master_arr)
print(test)
still_to_solve = unsolved_list(master_arr)

# actual loop
updates = 0
repeats = 0
'''while 0 in master_arr[0] and repeats < 81:
    for entry in still_to_solve:  # need to fix this idea of unsolved list
        r, c = entry
        add_this = 0
        if master_arr[10, r, c] == 1:
            add_this = np.max(master_arr[1:, r, c])
            update_whole(add_this, r, c, master_arr)
            still_to_solve.remove(entry)
            updates += 1
        else:
            # check naked pairs
            if master_arr[10, r, c] == 2:
                pair = []
                check_pair = []
                pair_exists = False
                col_to_check = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                row_to_check = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for number in master_arr[:9, r, c]:
                    if number != 0:  # get the pair of numbers that we are checking for
                        pair.append(number)
                col_to_check.remove(c)
                # pair = np.nonzero(master_arr[:9,r,c])

                # check if they occur in same row
                for col in col_to_check:  # check each col in row
                    # if this col only has two possibilities and they are the designated pair
                    if master_arr[10, r, col] == 2 and (
                            master_arr[pair[0], r, col] != 0 and master_arr[pair[1], r, col] != 0):
                        clear_row(pair[0], r, master_arr, [c, col])
                        clear_row(pair[1], r, master_arr, [c, col])  # remove these numbers from the rest of the row

                # check if they occur in same col
                for row in row_to_check:  # check each col in row
                    # if this row only has two possibilities and they are the designated pair
                    if master_arr[10, row, c] == 2 and (
                            master_arr[pair[0], row, c] != 0 and master_arr[pair[1], row, c] != 0):
                        clear_column(pair[0], c, master_arr, [r, row])
                        clear_column(pair[1], c, master_arr, [r, row])  # remove these numbers from the rest of the col

                # check if pair exists in same box


            # check hidden pairs
    repeats += 1'''

record_sheet.close()
