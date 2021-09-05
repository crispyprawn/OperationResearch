"""
@File  : simplex_decimal.py

@Author: no.1fansubgroup@gmail.com

@Date  : 2021/1/24

@Description  :
"""
from fractions import Fraction
import numpy as np
import sys
import pandas as pd


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
            continue
        intercepts.append(table[i][-1] / table[i][enter_col_index])

    intercepts_in_order = intercepts[:]
    intercepts_in_order.sort()
    for number in intercepts_in_order:
        if number > -1e-6:
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

    gauss_jordan_matrix = np.diag(np.full(dimension, 1))
    gauss_jordan_matrix = gauss_jordan_matrix.astype(np.float64)
    coefficients = table[:, pivot_column].copy()
    coefficients[pivot_row] = -1
    gauss_jordan_matrix[:, pivot_row] = -coefficients / table[pivot_row][pivot_column]
    # prepare the matrix used for gauss-jordan elimination
    table = np.dot(gauss_jordan_matrix, table)
    return table


def table_init_txt(filename):
    """
    create a nested list to represent the table from original data
    :param filename:
    :return:
    """
    file = open(filename, 'r')
    data = file.read().splitlines()

    simplex_tableau = []
    for row in data:
        simplex_tableau.append([float(x) for x in row.split()])

    return simplex_tableau


def table_init_csv(filename):
    """
    create a nested list to represent the table from data
    :param filename:
    :return:
    """
    return pd.read_csv(filename, header=None)


if __name__ == '__main__':
    sys.path.append("..")
    # simplex_table = np.array(table_init_txt('simplex_decimal.txt'))
    simplex_table = np.array(table_init_csv('simplex_decimal.csv'))
    np.set_printoptions(suppress=True)
    # to prevent extreme long decimal numbers
    print(simplex_table)
    iteration_count = 0

    while np.any(simplex_table[0] < -1e-6):
        # here the judgement condition is different from fractional version because of accuracy problem
        iteration_count += 1
        print(f"\n{iteration_count} iteration starts")
        p_column = np.argmin(simplex_table[0])
        p_row = decide_leaving(simplex_table, p_column)
        simplex_table = change(simplex_table, p_row, p_column)
        print(simplex_table)
        with open('outputfile.csv', 'ab') as f:
            np.savetxt(f, simplex_table, delimiter=',', fmt='%.04f')
    print("here is the optimal table!")
