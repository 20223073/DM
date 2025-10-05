import copy

# -----------------------------
# 1. 행렬 입력 함수
# -----------------------------
def input_matrix(n):
    print(f"\n{n}×{n}의 행렬 1행식 입력하세요. (띄어쓰기):")
    matrix = []
    for i in range(n):
        row = list(map(float, input(f"{i+1}행: ").split()))
        while len(row) != n:
            print(f"정확히 {n}개의 수를 입력하세요.")
            row = list(map(float, input(f"{i+1}행: ").split()))
        matrix.append(row)
    print(f"\n입력된 {n}×{n} 행렬 (리스트 형태):")
    print_matrix(matrix)
    return matrix

# -----------------------------
# 2. 행렬식(Determinant)
# -----------------------------
def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(submatrix)
    return det

# -----------------------------
# 3. 행렬식(수반행렬) 이용한 역행렬
# -----------------------------
def adjugate_inverse(matrix):
    n = len(matrix)
    det = determinant(matrix)
    if det == 0:
        raise ValueError("역행렬이 존재하지 않는다.")

    cofactors = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for i, row in enumerate(matrix) if i != r]
            cofactor = ((-1) ** (r + c)) * determinant(submatrix)
            cofactor_row.append(cofactor)
        cofactors.append(cofactor_row)

    adjugate = [[cofactors[c][r] for c in range(n)] for r in range(n)]
    inverse = [[adjugate[r][c] / det for c in range(n)] for r in range(n)]
    return inverse

# -----------------------------
# 4. 가우스-조던 소거법 이용한 역행렬
# -----------------------------
def gauss_jordan_inverse(matrix):
    n = len(matrix)
    a = copy.deepcopy(matrix)
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    for i in range(n):
        diag = a[i][i]
        if abs(diag) < 1e-12:
            raise ValueError("역행렬이 존재하지 않는다.")
        for j in range(n):
            a[i][j] /= diag
            I[i][j] /= diag
        for k in range(n):
            if k != i:
                factor = a[k][i]
                for j in range(n):
                    a[k][j] -= factor * a[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

# -----------------------------
# 5. 행렬 출력 (정수 형태로 리스트 출력)
# -----------------------------
def print_matrix(matrix):
    formatted_matrix = []
    for row in matrix:
        formatted_row = [int(round(x)) for x in row]
        formatted_matrix.append(formatted_row)
    print(formatted_matrix)

# -----------------------------
# 6. 두 행렬 비교
# -----------------------------
def compare_matrices(A, B, tol=1e-6):
    if len(A) != len(B):
        return False
    for i in range(len(A)):
        for j in range(len(A)):
            if abs(A[i][j] - B[i][j]) > tol:
                return False
    return True

# -----------------------------
# 메인 프로그램
# -----------------------------
print("=== 행렬의 역행렬 계산 프로그램 ===")

# (1) 2x2 역행렬 존재
matrix_2x2 = input_matrix(2)

# (2) 3x3 역행렬 존재
matrix_3x3_inv = input_matrix(3)

# (3) 3x3 특이행렬 (역행렬 없음)
matrix_3x3_sing = input_matrix(3)

# 전체 리스트(2차원 배열) 저장
matrix_list = [matrix_2x2, matrix_3x3_inv, matrix_3x3_sing]

# -----------------------------
# 각 행렬 처리 및 결과 출력
# -----------------------------
for idx, M in enumerate(matrix_list, start=1):
    print(f"\n==============================")
    print(f"[{idx}] 입력된 행렬:")
    print_matrix(M)
    det = determinant(M)
    print(f"행렬식 (Determinant): {int(round(det))}")

    try:
        inv1 = adjugate_inverse(M)
        print("\n[행렬식 이용 역행렬]")
        print_matrix(inv1)
    except ValueError as e:
        print("행렬식 이용 역행렬 계산 불가:", e)
        inv1 = None

    try:
        inv2 = gauss_jordan_inverse(M)
        print("\n[가우스-조던 이용 역행렬]")
        print_matrix(inv2)
    except ValueError as e:
        print("가우스-조던 역행렬 계산 불가:", e)
        inv2 = None

    if inv1 and inv2:
        same = compare_matrices(inv1, inv2)
        print(f"\n비교 결과: {'∴동일' if same else '다름'}")
    else:
        print("\n비교 결과: 두 방법 모두 계산 불가")
