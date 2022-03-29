#######################################################################################
## Author:          Phan Thanh Trung, Phan Ngoc Hung, Pham Nguyen Quang Khanh
##                  Tran Minh Quang, Dang Lam Tung
## Project:         [BGSV-HR-Chatbot]-Develop Chatbot for HR support
## Version:         4.0.0
## Maintainer:      Phan Ngoc Hung, Pham Nguyen Quang Khanh, Tran Minh Quang, Dang Lam Tung
## Status:          Work in Development and Maintenance
## Last modified:   March 17, 2022
## License:     
##    Copyright 2022, Robert Bosch Engineering & Business Solutions (RBVH)
## 
##    Licensed under the Apache License, Version 2.0 (the "License");
##    you may not use this file except in compliance with the License.
##    You may obtain a copy of the License at
## 
##        http://www.apache.org/licenses/LICENSE-2.0
##
##    Unless required by applicable law or agreed to in writing, software
##    distributed under the License is distributed on an "AS IS" BASIS,
##    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##    See the License for the specific language governing permissions and
##    limitations under the License.
#######################################################################################

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



def estimate_cosine_sim_two_vec(embedd_a, embedd_b):
    """Calculate the cosine similarity between two embedding vectors
        Note: Reshape a, b tensors to fit the requirements of scikit-learn
        X{ndarray, sparse matrix} of shape (n_samples_X, n_features)
        Y{ndarray, sparse matrix} of shape (n_samples_Y, n_features), default=None
    Args:
        embedd_a                        : np.ndarray
            The input embedding vector with the shape of (1, embedd_dim)
        embedd_b                        : np.ndarray
            The input embedding vector with the shape of (1, embedd_dim)
    Return:
        float
            The similarity between two input embedding vectors
    """
    
    # Estimate the cosine similarity with the sklearn's cosine function
    cosine_dist = cosine_similarity(embedd_a, embedd_b)

    return cosine_dist

def estimate_cosine_sim_vec_lst(embedd, embedd_lst):
    """
    Args:
        embedd                          : np.ndarray
            The input embedding vector with the shape of (1, embedd_dim)
        embedd_lst                      : list(np.ndarray)
            The list of input embedding vectors, each with the shape of (1, embedd_dim)
    Returns:
        List(float)
            The list of cosine similarity between input embedd vector and the given list
    """

    cosine_lst = []
    for embedd_i in embedd_lst:
        cosine_lst.append(estimate_cosine_sim_two_vec(embedd, embedd_i))
    return cosine_lst

def get_top_n_best_match_records(embedd_quest, embedd_lst, rec_lst, top_n=3):
    """Get the top-n best match data records (question, answer, distance) of the
        question embedding vectors and the list of embeddings from the corresponding intent
    Args:
    Returns:
    """

    # Estimate the cosine similarity between the question embedd & the given list
    cosine_sim_lst = estimate_cosine_sim_vec_lst(embedd_quest, embedd_lst)
    cosine_sim_mat = np.array([np.squeeze(dist) for dist in cosine_sim_lst])
    
    # Get the indices of top-n best matches
    best_n_indices = np.argsort(-cosine_sim_mat)[:top_n]
    # Construct the top-n best match data records (question, answer, distance)
    best_n_records = []
    for match_idx in best_n_indices:
        if rec_lst[match_idx][0].strip().endswith('?'):
            quest       = rec_lst[match_idx][0]
            ans         = rec_lst[match_idx][1]
            ans_id      = rec_lst[match_idx][2]
            distance    = cosine_sim_mat[match_idx]
            best_n_records.append((quest, ans, ans_id, distance))
        else:
            for rec in rec_lst:
                if rec_lst[match_idx][2] == rec[2] and rec[0].strip().endswith('?'):
                    quest       = rec[0]
                    ans         = rec[1]
                    ans_id      = rec[2]
                    distance    = cosine_sim_mat[match_idx]
                    best_n_records.append((quest, ans, ans_id, distance))
                    break

    return best_n_records

