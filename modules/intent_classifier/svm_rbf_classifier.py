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

import pickle
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn import svm

class SVM_TFIDF_Classifier:
    def __init__(
        self,
        pretrained,
        refit = True, 
        verbose = 1, 
        cv=5        
    ):
        
        # Initialize SVM model as a classifier
        svm_model = svm.SVC(probability=True) 

        # Define config for params
        param_grid = {'C': [ 1, 10, 100, 1000,10000], 
                    'gamma': [1,0.1,0.01,0.001,0.0001],
                    'kernel': ['linear']} 

        # Perform Grid search
        self.model = GridSearchCV(
            svm_model, 
            param_grid, 
            refit = refit, 
            verbose = verbose, 
            cv=cv
        )

        if not pretrained is None:
            self.load(pretrained)


    def fit(self, X, Y):
        """Perform hyper parameter tuning for model
        Args:
            X:          np.ndarray
                the TFIDF embeddings from input texts
            Y:          
                the label of the intent
        """

        best_model = self.model.fit(X, Y)
        # print(self.model.best_estimator_)
        self.model = best_model

        # Estimate the best accuracy
        train_accuracy = self.model.best_score_ *100
        print("Accuracy for our training dataset with tuning is : {:.2f}%".format(train_accuracy) )


    def predict(self, X):
        """Perform SVM prediction on TFIDF embeddings
        Args:
            X:          np.ndarray
                the TFIDF embeddings from input texts
        Returns:
            list[int]
                the list of predicted classes
        """
        return self.model.predict(X)

    def predict_prob(self, X, top_n=-1):
        """Perform SVM prediction on input embeddings and return the confidence scores of all classes
        Args:
            X:          np.ndarray
                the TFIDF embeddings from input texts
        Returns:
            List[List[Tuple(int, float)]]
                the outmost list is the list of samples
                the inner list is the list of classes
                each tuple presents the (class_idx, conf_score)
        """

        # Predict and Get the probabilities of all predicted classes
        probs = self.model.predict_proba(X)

        # Extract the indices of top-n class for all samples
        best_n = np.argsort(-probs, axis=1)[:, :top_n]

        # Extract the prediction results as tuples presenting the (class_idx, conf_score)
        prediction = []
        for sample_idx, sample_rank in enumerate(best_n):
            prediction.append([])
            for class_idx in sample_rank:
                prediction[-1].append((class_idx, probs[sample_idx, class_idx]))

        return prediction

    def save(self, path_to_save):
        # Save pretrained SVM predictor
        with open(path_to_save,'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path_to_load):
        # Load pretrained SVM predictor
        with open(path_to_load, 'rb') as f:
            self.model = pickle.load(f)

