import os
import numpy as np
import trimesh

from src.global_match.projection import project_to_sphere
from src.global_match.similarity import cosine_similarity
from src.preprocess.area_sample import area_weighted_sampling
from src.local_match.fpfh_compute import compute_fpfh
from src.local_match.local_similarity import local_fpfh_similarity


DATABASE_DIR = "data/database"


# ---------- GLOBAL DESCRIPTOR ----------
def compute_global_projection(stl_path):
    mesh = trimesh.load(stl_path, force="mesh")

    if len(mesh.faces) == 0:
        raise ValueError(f"Invalid STL: {stl_path}")

    num_faces = len(mesh.faces)
    num_points = min(max(2000, num_faces * 2), 12000)

    points = area_weighted_sampling(mesh, total_points=num_points)
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    return project_to_sphere(points)


# ---------- MAIN FUNCTION (FOR FLASK) ----------
def integrated_search(query_stl_path, top_k=10):
    """
    Runs global + local CAD similarity search.

    Returns:
    [
        {"name": "file.stl", "score": 0.82},
        ...
    ]
    """

    # ---- QUERY ----
    query_global = compute_global_projection(query_stl_path)
    _, query_fpfh = compute_fpfh(query_stl_path)

    # ---- GLOBAL SEARCH ----
    global_results = []

    for file in os.listdir(DATABASE_DIR):
        if not file.lower().endswith(".stl"):
            continue

        path = os.path.join(DATABASE_DIR, file)
        cand_global = compute_global_projection(path)
        g_score = cosine_similarity(query_global, cand_global)

        global_results.append((file, path, g_score))

    global_results.sort(key=lambda x: x[2], reverse=True)
    shortlist = global_results[:top_k]

    # ---- LOCAL + FUSION ----
    final_results = []

    for name, path, g_score in shortlist:
        _, cand_fpfh = compute_fpfh(path)
        l_score = local_fpfh_similarity(query_fpfh, cand_fpfh)

        final_score = 0.6 * g_score + 0.4 * l_score  # your fusion

        final_results.append({
            "name": name,
            "score": float(final_score)
        })

    final_results.sort(key=lambda x: x["score"], reverse=True)
    return final_results


# ---------- OPTIONAL CLI TEST ----------
if __name__ == "__main__":
    results = integrated_search("data/query/answercube.stl")

    print("\nFINAL RESULTS:\n")
    for r in results:
        print(r["name"], "→", r["score"])
