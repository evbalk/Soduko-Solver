# Soduko-Solver
This solves 4x4 and most 9x9 Soduko puzzles.
Currently working on adding method to solve for extreme cases where the location of multiple numbers cause one numbers placement.
The program creates 10 9x9 matrices, the 0th is the actual soduko layout while the nth matrix represents all the current legal placements of n in the soduko puzzle. For example, matrix 3 has the same layout as the actual soduko puzzle but it fills in every spot that a 3 could legally be placed in with a 3. Legality is determined by checking if n is already in the 0 matrix row or column, or if n is already in that r/c's box. Then it runs through each r,c in the matrix and checks if only one n matrix has a non-zero value there. This indicates that there is only one possible number than can be placed there.
It then updates the actual soduko with that information. Then it updates and recalculates all the n matrices to be in accordance with the 0 level matrix.
This method works for all 4x4 puzzles and easy-moderate 9x9 puzzles.
Extra methods used for the hard 9x9 include handling r,c locations where there are more than one option present. It then checks to see if for one of the options this is the only spot in the row to place it. If so, then it has to go there and override the other options. REpeat for the columns.
