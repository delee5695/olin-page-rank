"""
Description: Use google's page rank algorithm to order Olin College pages.
Name: Kenneth
Date: Discrete 2024
"""

import pickle
import numpy as np
from sklearn.preprocessing import normalize


def rank_pages(file_path, dapening_factor):
    with open(file_path, "rb") as file:
        # Load the data from the file
        olin_spider_dict = pickle.load(file)
    # create adjacency matrix
    url_index_dict = {key: idx for idx, key in enumerate(olin_spider_dict.keys())}
    transition_matrix = np.zeros(
        (len(olin_spider_dict.keys()), len(olin_spider_dict.keys()))
    )
    for key, backlink_list in olin_spider_dict.items():
        for url in backlink_list:
            if url in olin_spider_dict.keys():
                if url_index_dict[key] != url_index_dict[url]:
                    transition_matrix[url_index_dict[url], url_index_dict[key]] = 1
    # normalize so columns add to on
    stochastic_matrix = normalize(transition_matrix, axis=1, norm="l1")
    dapening_matrix = dapening_factor * (
        np.ones_like(stochastic_matrix) / stochastic_matrix.shape[1]
    )
    google_matrix = (1 - dapening_factor) * stochastic_matrix + dapening_matrix
    # calculate eigen vectors to rank the pages
    _, mat = np.linalg.eig(google_matrix)
    page_indices = np.argsort(-1 * mat[0])

    page_rank_index_list = []
    page_index_list = list(url_index_dict.keys())
    for idx, page in enumerate(page_indices):
        page_rank_index_list.append([page_index_list[page], idx])

    return page_rank_index_list
