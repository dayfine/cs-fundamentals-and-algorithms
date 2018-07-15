# https://www.wikiwand.com/en/Magic_square

from pprint import pprint

def magical_squre(n):
    if n <= 2:
        raise ValueError

    matrix = [[None] * n for _ in range(n)]

    i = n // 2
    j = n - 1

    num = 1
    while num <= n ** 2:
        matrix[i][j] = num
        num += 1

        ni, nj = (i - 1) % n, (j + 1) % n
        if matrix[ni][nj]:
            ni, nj = i, (j - 1) % n

        i, j = ni, nj

    pprint(matrix)

magical_squre(3)
magical_squre(4)
magical_squre(5)
magical_squre(6)
magical_squre(7)
