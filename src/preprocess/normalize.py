import trimesh
import numpy as np

mesh = trimesh.load(
    r"D:\Gowthamroyal UG student\Projects\cad-similarity-engine\data\query\answercube.stl")
points = mesh.sample(5000)

centroid = points.mean(axis=0)
points_centered = points - centroid

max_dist = np.linalg.norm(points_centered, axis=1).max()
points_normalized = points_centered / max_dist

print("Centroid:", centroid)
print("Max distance after scaling:", np.linalg.norm(
    points_normalized, axis=1).max())
print("First 5 normalized points:")
print(points_normalized[:10])
