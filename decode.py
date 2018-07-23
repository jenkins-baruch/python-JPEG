import encode


def un_quantization(matrix):
    return (
        (matrix[row][col]*encode.quantization_matrix[row][col]
         for col in range(len(matrix[row])))
        for row in range(len(matrix))
    )


def inverse_DCT(matrix):
    pass
