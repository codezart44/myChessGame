# TEST DOC
import numpy as np


# mystring = "TheNameIsBond,JamesBond"

# mystring = "".join([l if l.islower() or l == ',' else f" {l.lower()}" if l in ['N', 'I'] else f" {l}" for l in mystring])[1:]

# print(mystring)

myarray = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7],
    [10, 11, 12, 13, 14, 15, 16, 17],
    [20, 21, 22, 23, 24, 25, 26, 27],
    [30, 31, 32, 33, 34, 35, 36, 37],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [50, 51, 52, 53, 54, 55, 56, 57],
    [60, 61, 62, 63, 64, 65, 66, 67],
    [70, 71, 72, 73, 74, 75, 76, 77]
    ])


# truth = np.array([True, True, True, True])
# print(truth.all())



# mymatrix = np.matrix([
#     [0, 1, 2, 3, 4, 5, 6, 7],
#     [10, 11, 12, 13, 14, 15, 16, 17],
#     [20, 21, 22, 23, 24, 25, 26, 27],
#     [30, 31, 32, 33, 34, 35, 36, 37],
#     [40, 41, 42, 43, 44, 45, 46, 47],
#     [50, 51, 52, 53, 54, 55, 56, 57],
#     [60, 61, 62, 63, 64, 65, 66, 67],
#     [70, 71, 72, 73, 74, 75, 76, 77]
# ])



# print(all([True if square=='-' else False for square in myarray]))

segment = myarray[1:4, 1:4]

if True:
    segment = np.rot90(segment)

print(segment)

# print(np.diag(myarray[1:4, 1:4]))
# print()
# print(np.rot90(myarray[1:4, 1:4]))
# print(np.diag(np.rot90(myarray[1:4, 1:4])))





""" Sketch

00 01 02 03 04 05 06 07
10 11 12 13 14 15 16 17
20 21 22 23 24 25 26 27
30 31 32 33 34 35 36 37
40 41 42 43 44 45 46 47
50 51 52 53 54 55 56 57
60 61 62 63 64 65 66 67
70 71 72 73 74 75 76 77

"""