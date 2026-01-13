import numpy as np
from scipy.spatial import cKDTree


def local_fpfh_similarity(fpfh_query, fpfh_candidate, distance_thresh=0.25):
    """
    Compute local similarity score using FPFH nearest-neighbor matching.

    Parameters:
        fpfh_query: (Nq, 33) ndarray
        fpfh_candidate: (Nc, 33) ndarray
        distance_thresh: float (matching threshold)

    Returns:
        local_similarity: float in [0, 1]
    """

    if fpfh_query.size == 0 or fpfh_candidate.size == 0:
        return 0.0

    # Build KD-tree on candidate descriptors
    tree = cKDTree(fpfh_candidate)

    # Query nearest neighbors
    distances, _ = tree.query(fpfh_query, k=1)

    # Count good matches
    good_matches = np.sum(distances < distance_thresh)

    # Normalize
    local_similarity = good_matches / len(fpfh_query)

    return float(local_similarity)
