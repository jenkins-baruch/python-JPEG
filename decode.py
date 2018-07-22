import encode


def un_quantization(matrix):
    return ((matrix[row][col] * encode.quantization_matrix[row][col]
             for col in range(len(matrix[row])))
            for row in range(len(matrix)))


def __f_xy(x, y, matrix):
    return round(sum(
        encode.alpha(u) * encode.alpha(v) * matrix[u][v] *
        encode.cos_element(x, u) * encode.cos_element(y, v)
        for u in range(len(matrix[0]))
        for v in range(len(matrix))) / 4)


def inverse_DCT(matrix):
    return ((__f_xy(x, y, matrix)
             for x in range(len(matrix[y])))
            for y in range(len(matrix)))


def un_normalize(matrix):
    return ((cell + 128 for cell in row) for row in matrix)
