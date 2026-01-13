import numpy as np
import trimesh
import open3d as o3d

from src.preprocess.area_sample import area_weighted_sampling


def compute_fpfh(stl_path):
    # 1. Load STL using trimesh
    mesh = trimesh.load(stl_path, force='mesh')

    if len(mesh.faces) == 0:
        raise ValueError("Invalid STL: no faces")

    # 2. Adaptive sampling (same logic as global)
    num_faces = len(mesh.faces)
    num_points = min(max(2000, num_faces * 2), 12000)

    points = area_weighted_sampling(mesh, total_points=num_points)

    # 3. Normalize
    points -= points.mean(axis=0)
    points /= np.linalg.norm(points, axis=1).max() + 1e-8

    # 4. Convert to Open3D PointCloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # 5. Estimate normals
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.05,
            max_nn=30
        )
    )

    # 6. Compute FPFH
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1,
            max_nn=100
        )
    )

    # Open3D returns (33, N) → transpose
    fpfh_features = np.asarray(fpfh.data).T

    return points.shape[0], fpfh_features


if __name__ == "__main__":
    stl_path = "data/query/answercube.stl"

    n_points, fpfh = compute_fpfh(stl_path)

    print("Number of points:", n_points)
    print("FPFH shape:", fpfh.shape)
