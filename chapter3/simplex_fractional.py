import json
from fractions import Fraction
import numpy as np
import sys


def decide_leaving(table, enter_col_index):
    """
    decide the leaving variable

    :argument:
        table: a standard two-dimensional table for simplex method
        enter_col_index: the column index of the entering variable

    :returns:
        the column index of variable that has the minimal positive ratio of solution column
        over entering variable's coefficient column
    """
    intercepts = []
    for i in range(1, len(table)):
        if table[i][enter_col_index] <= 0:
            intercepts.append(-1)
        else:
            intercepts.append(Fraction(table[i][-1], table[i][enter_col_index]))

    intercepts_in_order = intercepts[:]
    intercepts_in_order.sort()
    for number in intercepts_in_order:
        if number > 0:
            return intercepts.index(number) + 1


def change(table, pivot_row, pivot_column):
    """
    do the gauss-jordan elimination so that the basic variable changes

    :argument:
        table: the standard 2-dimensional table for simplex method
        pivot_row: row index of the pivot
        pivot_column: column index of the pivot

    :returns:
        the simplex table after one iteration
    """
    dimension = len(table)

    gauss_jordan_matrix = np.diag(np.full(dimension, Fraction(1)))
    coefficients = table[:, pivot_column].copy()
    coefficients[pivot_row] = Fraction(-1)
    gauss_jordan_matrix[:, pivot_row] = -coefficients / table[pivot_row][pivot_column]
    # prepare the matrix used for gauss-jordan elimination
    table = np.dot(gauss_jordan_matrix, table)
    return table


def table_init(filename):
    """
    create a nested list to represent the table from original data, convert integer to fractions
    :param filename:
    :return:
    """
    file = open(filename, 'r')
    data = file.read().splitlines()

    simplex_tableau = []
    for row in data:
        line = row_initialize(row)
        simplex_tableau.append(line)

    return simplex_tableau


def row_initialize(original):
    row_in_integer = original.split()
    row_in_fraction = []
    for coefficient in row_in_integer:
        row_in_fraction.append(Fraction(coefficient))
    return row_in_fraction


def handle_request(matrix):
    np_matrix = np.array([[Fraction(num) for num in row] for row in matrix])
    iteration_times = 0
    iteration = dict()
    print(np_matrix)
    while np.any(np_matrix[0] < 0):
        iteration_times += 1
        pivot_col = np.argmin(np_matrix[0])
        pivot_row = decide_leaving(np_matrix, pivot_col)
        np_matrix = change(np_matrix, pivot_row, pivot_col)
        print(np_matrix)
        iteration[iteration_times] = json.dumps([[(num.numerator, num.denominator) for num in row] for row in np_matrix])

    return iteration


if __name__ == '__main__':
    sys.path.append("..")
    simplex_table = np.array(table_init('simplex_fractional.txt'))
    iteration_count = 0

    while np.any(simplex_table[0] < 0):
        iteration_count += 1
        print(f"{iteration_count} iteration starts")
        p_column = np.argmin(simplex_table[0])
        p_row = decide_leaving(simplex_table, p_column)
        simplex_table = change(simplex_table, p_row, p_column)
        print(simplex_table)

    print("here is the optimal table!")
