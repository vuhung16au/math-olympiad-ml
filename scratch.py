A = [
    [0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 1, 1, 0]
]

def matmul(X, Y):
    result = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            for k in range(5):
                result[i][j] += X[i][k] * Y[k][j]
    return result

A2 = matmul(A, A)
A3 = matmul(A2, A)

print("A2:")
for row in A2: print(row)
print("A3:")
for row in A3: print(row)
print("Trace A3:", sum(A3[i][i] for i in range(5)))
