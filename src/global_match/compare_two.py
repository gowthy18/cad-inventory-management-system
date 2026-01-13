import numpy as np
import trimesh

from src.global_match.projection import project_to_sphere
from src.global_match.similarity import cosine_similarity


def compute_projection(stl_path, n_points=5000):
    mesh = trimesh.load(stl_path, force='mesh')

    if len(mesh.faces) == 0:
        raise ValueError(f"Invalid mesh: {stl_path}")

    points = mesh.sample(n_points)

    # normalize
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    return project_to_sphere(points)


if __name__ == "__main__":

    # 🔴 CHANGE THESE TWO FILES 🔴
    query_stl = "data/query/answercube.stl"
    candidate_stl = "data/query/answercube.stl"  # try a different one later

    proj_query = compute_projection(query_stl)
    proj_candidate = compute_projection(candidate_stl)

    score = cosine_similarity(proj_query, proj_candidate)

    print("Global similarity score:", score)
