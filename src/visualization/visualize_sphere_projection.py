import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.global_match.projection import project_to_sphere


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError(
            "Usage: python -m src.visualization.visualize_sphere_projection <path_to_stl>"
        )

    STL_PATH = sys.argv[1]

    # =========================================================
    # 1️⃣ Load mesh
    # =========================================================
    mesh = trimesh.load(STL_PATH, force="mesh")

    # =========================================================
    # 2️⃣ Sample surface points WITH face indices
    # =========================================================
    points, face_idx = trimesh.sample.sample_surface(mesh, 2000)

    # =========================================================
    # 3️⃣ Normalize (centering + unit sphere)
    # =========================================================
    points = points - points.mean(axis=0)
    points = points / (np.linalg.norm(points, axis=1).max() + 1e-8)

    # =========================================================
    # 🔵 CENTER PROJECTION (radial)
    # =========================================================
    proj_center_3d = points / np.linalg.norm(points, axis=1, keepdims=True)
    proj_center_2d = project_to_sphere(proj_center_3d)

    # =========================================================
    # 🔴 NORMAL-DIRECTION PROJECTION (face normals)
    # =========================================================
    normals = mesh.face_normals[face_idx]

    proj_normal_3d = points + normals
    proj_normal_3d = proj_normal_3d / np.linalg.norm(
        proj_normal_3d, axis=1, keepdims=True
    )

    proj_normal_2d = project_to_sphere(proj_normal_3d)

    # =========================================================
    # 📊 PAPER-STYLE VISUALIZATION
    # =========================================================
    fig = plt.figure(figsize=(10, 8))

    # ---- Normal-direction sphere ----
    ax1 = fig.add_subplot(221, projection="3d")
    ax1.scatter(
        proj_normal_3d[:, 0],
        proj_normal_3d[:, 1],
        proj_normal_3d[:, 2],
        s=2
    )
    ax1.set_title("Normal Direction Projection")
    ax1.set_axis_off()

    # ---- Center-projection sphere ----
    ax2 = fig.add_subplot(222, projection="3d")
    ax2.scatter(
        proj_center_3d[:, 0],
        proj_center_3d[:, 1],
        proj_center_3d[:, 2],
        s=2
    )
    ax2.set_title("Center Projection")
    ax2.set_axis_off()

    # ---- Normal-direction matrix ----
    ax3 = fig.add_subplot(223)
    ax3.imshow(proj_normal_2d, cmap="viridis")
    ax3.set_title("Transformation into Matrix (Normal)")
    ax3.axis("off")

    # ---- Center-projection matrix ----
    ax4 = fig.add_subplot(224)
    ax4.imshow(proj_center_2d, cmap="viridis")
    ax4.set_title("Transformation into Matrix (Center)")
    ax4.axis("off")

    plt.tight_layout()
    plt.show()
