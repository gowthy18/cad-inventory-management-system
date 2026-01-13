# main.py
from src.global_match.projection import project_to_sphere
from src.global_match.similarity import cosine_similarity
from src.preprocess.area_sample import area_weighted_sampling
import trimesh
import numpy as np


def compute_projection(stl_path):
    mesh = trimesh.load(stl_path, force='mesh')
    if len(mesh.faces) == 0:
        raise ValueError("STL has no faces")

    # adaptive sampling by mesh size
    num_faces = len(mesh.faces)
    num_points = min(max(2000, num_faces * 2), 12000)

    points = area_weighted_sampling(mesh, total_points=num_points)
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    return project_to_sphere(points)


if __name__ == "__main__":
    query = "data/query/answercube.stl"
    cand = "data/query/answercube.stl"

    Pq = compute_projection(query)
    Pc = compute_projection(cand)

    score = cosine_similarity(Pq, Pc)
    print("Global similarity score:", score)
