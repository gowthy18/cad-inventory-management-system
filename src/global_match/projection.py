import numpy as np
import trimesh

from src.preprocess.area_sample import area_weighted_sampling


def project_to_sphere(points, n_theta=32, n_phi=64):
    x, y, z = points[:, 0], points[:, 1], points[:, 2]

    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x)

    theta_idx = (theta / np.pi * n_theta).astype(int)
    phi_idx = ((phi + np.pi) / (2 * np.pi) * n_phi).astype(int)

    theta_idx = np.clip(theta_idx, 0, n_theta - 1)
    phi_idx = np.clip(phi_idx, 0, n_phi - 1)

    mat = np.zeros((n_theta, n_phi), dtype=np.float32)
    for t, p in zip(theta_idx, phi_idx):
        mat[t, p] += 1.0

    mat /= mat.sum() + 1e-8
    return mat


if __name__ == "__main__":

    # 🔴 STL INPUT 🔴
    mesh = trimesh.load("data/query/answercube.stl", force='mesh')

    print("Vertices:", len(mesh.vertices))
    print("Faces:", len(mesh.faces))

    if len(mesh.faces) == 0:
        raise ValueError("STL has no faces")

    # 🔹 ADAPTIVE SAMPLING BASED ON MESH SIZE
    num_faces = len(mesh.faces)
    num_points = min(
        max(2000, num_faces * 2),
        12000
    )

    print("Sampling points:", num_points)

    points = area_weighted_sampling(mesh, total_points=num_points)

    # 🔹 NORMALIZATION
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    # 🔹 PROJECTION
    proj = project_to_sphere(points)

    print("Projection matrix shape:", proj.shape)
    print("Matrix sum:", proj.sum())
