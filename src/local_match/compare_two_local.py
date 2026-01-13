from src.local_match.fpfh_compute import compute_fpfh
from src.local_match.local_similarity import local_fpfh_similarity


if __name__ == "__main__":

    query_stl = "data/query/answercube.stl"
    candidate_stl = "data/database/answercube.stl"

    _, fpfh_q = compute_fpfh(query_stl)
    _, fpfh_c = compute_fpfh(candidate_stl)

    score = local_fpfh_similarity(fpfh_q, fpfh_c)

    print("Local similarity score:", score)
