import numpy as np


def cosine_similarity(mat1, mat2):
    """
    mat1, mat2: projection matrices of same shape
    returns: similarity score in [0, 1]
    """

    v1 = mat1.flatten()
    v2 = mat2.flatten()

    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)

    if den == 0:
        return 0.0

    return num / den


if __name__ == "__main__":
    # quick self-test
    A = np.random.rand(32, 64)
    A /= A.sum()

    B = A.copy()

    sim = cosine_similarity(A, B)
    print("Similarity (should be ~1):", sim)
