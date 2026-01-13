import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.preprocess.area_sample import area_weighted_sampling


STL_PATH = "data/query/answercube.stl"


if __name__ == "__main__":

    mesh = trimesh.load(STL_PATH, force="mesh")

    points = area_weighted_sampling(mesh, total_points=2000)

    fig = plt.figure(figsize=(10, 5))

    # Raw vertices
    ax1 = fig.add_subplot(121, projection="3d")
    ax1.scatter(
        mesh.vertices[:, 0],
        mesh.vertices[:, 1],
        mesh.vertices[:, 2],
        s=1
    )
    ax1.set_title("Raw STL Vertices")

    # Sampled points
    ax2 = fig.add_subplot(122, projection="3d")
    ax2.scatter(
        points[:, 0],
        points[:, 1],
        points[:, 2],
        s=3
    )
    ax2.set_title("Area-Weighted Sampled Points")

    plt.show()
