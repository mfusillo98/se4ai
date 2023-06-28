from sklearn.decomposition import PCA
import numpy as np


def get_best_features_indexes(data, min_explained_variance=0.95):
    components = min(800, len(data))  # for testing purpose len(image_features) could be less than 300
    pca = PCA(n_components=components)
    pca.fit_transform(data)
    best_features_idxs = []
    cumulative_explained_variance = 0
    for i in range(0, len(pca.explained_variance_ratio_)):
        # Retrieving the variance explained by the i-th component
        variance = pca.explained_variance_ratio_[i]
        cumulative_explained_variance = cumulative_explained_variance + variance
        # Getting the index of the best (not already picked) feature of the i-th component
        feat_idx = get_argmax_index_with_blacklist(pca.components_[i], best_features_idxs)
        if feat_idx is not None:
            best_features_idxs.append(feat_idx)
        if cumulative_explained_variance >= min_explained_variance:
            return best_features_idxs
    return best_features_idxs


def get_argmax_index_with_blacklist(items, blacklist_indexes):
    max_idx = None
    for i in range(0, len(items)):
        if i not in blacklist_indexes:
            if max_idx is None or abs(items[i]) > abs(items[max_idx]):  # PCA sign does not affect its interpretation since the sign does not affect the variance contained in each component. Only the relative signs of features forming the PCA dimension are important.
                max_idx = i
    return max_idx
