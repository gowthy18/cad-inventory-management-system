import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.preprocess.area_sample import area_weighted_sampling


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError(
            "Usage: python -m src.visualization.visualize_normalization <path_to_stl>"
        )

    STL_PATH = sys.argv[1]

    mesh = trimesh.load(STL_PATH, force="mesh")
    points = area_weighted_sampling(mesh, total_points=2000)

    # Normalize
    centered = points - points.mean(axis=0)
    normalized = centered / (np.linalg.norm(centered, axis=1).max() + 1e-8)

    fig = plt.figure(figsize=(10, 5))

    ax1 = fig.add_subplot(121, projection="3d")
    ax1.scatter(points[:, 0], points[:, 1], points[:, 2], s=3)
    ax1.set_title("Before Normalization")

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.scatter(
        normalized[:, 0],
        normalized[:, 1],
        normalized[:, 2],
        s=3
    )
    ax2.set_xlim([-1, 1])
    ax2.set_ylim([-1, 1])
    ax2.set_zlim([-1, 1])
    ax2.set_title("After Unit-Sphere Normalization")

    plt.show()
