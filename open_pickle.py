import pickle
import numpy as np
from sklearn.preprocessing import normalize


dapening_factor = 0.15
with open("outlinks-dict.pickle", "rb") as file:
    # Load the data from the file
    olin_spider_dict = pickle.load(file)
# normalized adjacency matrix where rows are teh sites, and columns are the sites that reference a given row
url_index_dict = {key: idx for idx, key in enumerate(olin_spider_dict.keys())}
transition_matrix = np.zeros(
    (len(olin_spider_dict.keys()), len(olin_spider_dict.keys()))
)
for key, backlink_list in olin_spider_dict.items():
    for url in backlink_list:
        if url in olin_spider_dict.keys():
            if url_index_dict[key] != url_index_dict[url]:
                transition_matrix[url_index_dict[url], url_index_dict[key]] = 1
stochastic_matrix = normalize(transition_matrix, axis=1, norm="l1")
dapening_matrix = dapening_factor * (
    np.ones_like(stochastic_matrix) / stochastic_matrix.shape[1]
)
google_matrix = (1 - dapening_factor) * stochastic_matrix + dapening_matrix

val, mat = np.linalg.eig(google_matrix)

# print(np.sum(google_matrix, axis=1))

print(mat[0])
print(np.argmax(mat[0]))
print(len(olin_spider_dict[list(url_index_dict.keys())[np.argmax(mat[0])]]))
# print(np.sum(stochastic_matrix, axis=1))
