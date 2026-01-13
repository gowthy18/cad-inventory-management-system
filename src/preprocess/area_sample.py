import numpy as np


def area_weighted_sampling(mesh, total_points):
    """
    Deterministic area-weighted surface sampling
    """

    faces = mesh.faces
    vertices = mesh.vertices
    face_areas = mesh.area_faces
    total_area = face_areas.sum()

    points_per_face = np.maximum(
        (face_areas / total_area * total_points).astype(int),
        1
    )

    sampled_points = []

    for face, n_pts in zip(faces, points_per_face):
        v0, v1, v2 = vertices[face]

        for i in range(n_pts):
            a = (i + 0.5) / n_pts
            b = 1.0 - a
            p = a * v0 + b * v1
            sampled_points.append(p)

            if len(sampled_points) >= total_points:
                break

        if len(sampled_points) >= total_points:
            break

    return np.array(sampled_points[:total_points])
