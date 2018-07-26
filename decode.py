import dct


def un_quantization(matrix):
    return ((matrix[row][col] * encode.quantization_matrix[row][col]
             for col in range(len(matrix[row])))
            for row in range(len(matrix)))


def un_normalize(matrix):
    return ((cell + 128 for cell in row) for row in matrix)
