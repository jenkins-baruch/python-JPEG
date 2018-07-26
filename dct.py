import math


def __cos_element(x, u):
    return math.cos((2 * x + 1) * u * math.pi / 16)


def __alpha(u):
    return 1 / math.sqrt(2) if u == 0 else 1


def __G_uv(u, v, matrix):
    return (1 / 4) * __alpha(u) * __alpha(v) * sum(
        matrix[x][y] * __cos_element(x, u) * __cos_element(y, v)
        for x in range(len(matrix))
        for y in range(len(matrix[0])))


def discerete_cosine_transform(matrix):
    return ((round(__G_uv(y, x, matrix), 2)
             for x in range(len(matrix[y])))
            for y in range(len(matrix)))


def __f_xy(x, y, matrix):
    return round(
        0.25 *
        sum(
            __alpha(u) * __alpha(v) * matrix[v][u] *
            __cos_element(x, u) * __cos_element(y, v)
            for u in range(len(matrix[0]))
            for v in range(len(matrix)))
    )


def inverse_DCT(matrix):
    return ((__f_xy(x, y, matrix)
             for x in range(len(matrix[y])))
            for y in range(len(matrix)))
