import os
import trimesh
import numpy as np

from src.global_match.projection import project_to_sphere
from src.global_match.similarity import cosine_similarity
from src.preprocess.area_sample import area_weighted_sampling


def compute_projection(stl_path):
    mesh = trimesh.load(stl_path, force='mesh')

    if len(mesh.faces) == 0:
        raise ValueError(f"Invalid STL: {stl_path}")

    num_faces = len(mesh.faces)
    num_points = min(max(2000, num_faces * 2), 12000)

    points = area_weighted_sampling(mesh, total_points=num_points)
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    return project_to_sphere(points)


if __name__ == "__main__":

    # 🔴 PATHS 🔴
    QUERY_STL = "data/query/answercube.stl"

    DATABASE_DIR = "data/database"

    # compute query projection ONCE
    query_proj = compute_projection(QUERY_STL)

    results = []

    for file in os.listdir(DATABASE_DIR):
        if not file.lower().endswith(".stl"):
            continue

        stl_path = os.path.join(DATABASE_DIR, file)

        db_proj = compute_projection(stl_path)
        score = cosine_similarity(query_proj, db_proj)

        results.append((file, score))

    # sort by similarity (high → low)
    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🔍 Top matches:\n")
    for name, score in results[:5]:
        print(f"{name:30s}  similarity = {score:.4f}")
