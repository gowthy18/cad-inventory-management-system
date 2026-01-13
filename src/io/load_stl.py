import trimesh
import numpy as np

mesh = trimesh.load(
    r"D:\Gowthamroyal UG student\Projects\cad-similarity-engine\data\query\answercube.stl")


vertices = mesh.vertices

print("Total vertices:", len(vertices))
print("First 5 vertices:")
print(vertices[:5])
