import pickle
import numpy as np


def __loadlsh__(lsh_path):
    with open(lsh_path, 'rb') as filehandle:
        lsh = pickle.load(filehandle)
    return lsh


def __cosine_sim(vec1, vec2):
    return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
