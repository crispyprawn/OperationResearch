import chapter3.initialize as pre
import numpy as np


def pre_processing(table):
    base = np.full(table.shape, 1)
    # if the data contains fractions, just change 1 to Fraction(1), but the calculations will be slow

    row_min = table.min(axis=1)
    row_eigen_matrix = np.diag(row_min)
    table = table - np.dot(row_eigen_matrix, base)

    col_min = table.min(axis=0)
    col_eigen_matrix = np.diag(col_min)
    table = table - np.dot(base, col_eigen_matrix)

    return table


def attempt_assign(table):
    while table_has_single_zero(table):
        process_row_with_single_zero(table)
        table = table.T

        process_row_with_single_zero(table)
        table = table.T
    while table_has_zero(table):
        process_final_zeros(table)


def find_final_row(table):
    zeros_remain = []
    for row in table:
        zeros_remain.append(zeros_in_row(row))
    zeros_remain_sort = zeros_remain[:]
    zeros_remain_sort.sort()
    final_row_zeros = 0
    for zero_number in zeros_remain_sort:
        if zero_number > 0:
            final_row_zeros = zero_number
            break
    for i in range(len(table)):
        if zeros_in_row(table[i]) == final_row_zeros:
            return i


def find_final_col(table, final_row_index):
    zeros_remain = []
    for task in range(len(table[0])):
        if table[final_row_index][task] == 0:
            zeros_remain.append(zeros_in_col(table, task))
    zeros_remain.sort()
    final_col_zeros = zeros_remain[0]
    for task in range(len(table[0])):
        if zeros_in_col(table, task) == final_col_zeros and table[final_row_index][task] == 0:
            return task


def process_final_zeros(table):
    final_row_index = find_final_row(table)
    final_col_index = find_final_col(table, final_row_index)
    for people in range(len(table)):
        if table[people][final_col_index] == 0:
            table[people][final_col_index] = -2
    #          if the data contains fractions, just change -2 to Fraction(-2), but the calculations will be slow
    for task in range(len(table[0])):
        if table[final_row_index][task] == 0:
            table[final_row_index][task] = -2
    table[final_row_index][final_col_index] = -1


def zeros_in_row(row):
    zeros = 0
    for number in row:
        if number == 0:
            zeros += 1
    return zeros


def negative_one_in_row(row):
    negative_ones = 0
    for number in row:
        if number == -1:
            negative_ones += 1
    return negative_ones


def zeros_in_col(table, col_index):
    zeros = 0
    for each_row in table:
        if each_row[col_index] == 0:
            zeros += 1
    return zeros


def index_of_unique_zero(table, col_index):
    for row_index in range(len(table)):
        if table[row_index][col_index] == 0:
            return row_index


def process_row_with_single_zero(table):
    for row in table:
        if np.count_nonzero(row == 0) == 1:
            task = np.argwhere(row == 0)[0][0]
            row[task] = -1
            for person in range(len(table)):
                if table[person][task] == 0:
                    table[person][task] = -2


def process_col_with_single_zero(table):
    for col in range(len(table[0])):
        if zeros_in_col(table, col) == 1:
            row = index_of_unique_zero(table, col)
            table[row][col] = -1
            for task in range(len(table[0])):
                if table[row][task] == 0:
                    table[row][task] = -2


def table_has_single_zero(table):
    row_zeros = np.count_nonzero(table == 0, axis=1)
    if np.any(row_zeros == 1):
        return True

    col_zeros = np.count_nonzero(table == 0, axis=0)
    if np.any(col_zeros == 1):
        return True

    return False


def table_has_zero(table):
    for row in table:
        for item in row:
            if item == 0:
                return True
    return False


def tick_table(table):
    new_ticks = 0
    tick_rows = []
    tick_cols = []
    for row_index in range(len(table)):
        if negative_one_in_row(table[row_index]) == 0:
            tick_rows.append(row_index)
            new_ticks += 1
    while new_ticks != 0:
        new_ticks = 0
        for already_tick_row in tick_rows:
            for task in range(len(table[0])):
                if table[already_tick_row][task] == -2 and (task not in tick_cols):
                    tick_cols.append(task)
                    new_ticks += 1
        for already_tick_col in tick_cols:
            for people in range(len(table)):
                if table[people][already_tick_col] == -1 and (people not in tick_rows):
                    tick_rows.append(people)
                    new_ticks += 1

    tick_rows.sort()
    tick_cols.sort()
    return tick_rows, tick_cols


def need_increase_zero(table, ticked_rows, ticked_cols):
    line_row_number = len(table) - len(ticked_rows)
    line_col_number = len(ticked_cols)
    if line_row_number + line_col_number == len(table):
        return False
    else:
        return True


def increase_zero(table, ticked_rows, ticked_cols):
    not_crossed = []
    for i in range(len(table)):
        for j in range(len(table[0])):
            if (i in ticked_rows) and (j not in ticked_cols):
                not_crossed.append(table[i][j])
    not_crossed.sort()
    min_not_crossed = not_crossed[0]
    for i in ticked_rows:
        for j in range(len(table[0])):
            table[i][j] -= min_not_crossed
    for j in ticked_cols:
        for i in range(len(table)):
            table[i][j] += min_not_crossed
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == -1:
                table[i][j] += 1
            if table[i][j] == -2:
                table[i][j] += 2


def table_init(filename):
    file = open(filename, 'r')
    data = file.read().splitlines()

    simplex_tableau = []
    for i in range(len(data)):
        line = data[i].split()
        simplex_tableau.append(line)

    return simplex_tableau


if __name__ == '__main__':
    first_table = np.array(table_init('../hungarian_matrix.txt'))
    print(first_table)
    first_table = pre_processing(first_table)
    print("pre processed")
    attempt_assign(first_table)
    print(first_table)
    print(tick_table(first_table))
    ticked_row, ticked_col = tick_table(first_table)
    print(need_increase_zero(first_table, ticked_row, ticked_col))
    while need_increase_zero(first_table, ticked_row, ticked_col):
        increase_zero(first_table, ticked_row, ticked_col)
        print(first_table)
        attempt_assign(first_table)
        print(first_table)
        ticked_row, ticked_col = tick_table(first_table)
        print(tick_table(first_table))
