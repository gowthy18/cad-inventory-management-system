import trimesh
import numpy as np

mesh = trimesh.load(
    r"D:\Gowthamroyal UG student\Projects\cad-similarity-engine\data\query\answercube.stl")
points = mesh.sample(5000)

print("Total sampled points:", len(points))
print("First 5 sampled points:")
print(points[:5])
