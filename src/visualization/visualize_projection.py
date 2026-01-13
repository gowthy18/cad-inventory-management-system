import numpy as np
import trimesh
import matplotlib.pyplot as plt

from src.preprocess.area_sample import area_weighted_sampling
from src.global_match.projection import project_to_sphere


STL_PATH = "data/query/answercube.stl"


if __name__ == "__main__":

    mesh = trimesh.load(STL_PATH, force="mesh")
    points = area_weighted_sampling(mesh, total_points=2000)

    # Normalize
    points = points - points.mean(axis=0)
    points = points / (np.linalg.norm(points, axis=1).max() + 1e-8)

    proj = project_to_sphere(points)

    plt.figure(figsize=(6, 4))
    plt.imshow(proj, cmap="hot")
    plt.colorbar(label="Point Density")
    plt.title("Spherical Projection Descriptor")
    plt.xlabel("Phi bins")
    plt.ylabel("Theta bins")
    plt.show()
