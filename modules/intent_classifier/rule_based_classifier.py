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

import pandas as pd
import numpy as np
import spacy
from spacy.matcher import PhraseMatcher



class RuleBasedClassifier:
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.nlp = spacy.load("en_core_web_sm")
       
    def read_signature_data_from_file(self):
        """Read data from csv and convert to a dict
        Returns:
            Dict
                a dictionary to store the keywords for each intent topic
                {   
                    'Recruitment process': [],
                    'Recruitment procedure': [],
                    'internship policy': [],
                    'Referral Rewards Policy': [],
                    'Rehire ex-Boschlers': [],
                    'Relocation Support/Expat': [],
                    'Talent hub': [],
                    'Recruitment Needs': [],
                    'HR policy': []
                }
        """
        data = pd.read_csv(self.data_path, encoding = 'unicode_escape')
        
        keyword = data['Word'].tolist()
        labels = data['Intent'].tolist()
        
        if not len(keyword) == len(labels):
            raise ValueError('The number of keyword and intent is not match, please check your data again')
        
        # Convert a list of label to a list of label indices
        label_dict = dict(
            zip(
                sorted(set(labels), key=labels.index), 
                range(len(labels))
            )
        )
        label_set = sorted(set(labels), key=labels.index)

        # Convert label from string to numeric indices
        label_indices=[label_dict[label] for label in labels]
        
        key_dict = {}
        for names in label_set:
            key_dict[names] = []
            
        for word, label_name in zip(keyword, labels):
            key_dict[label_name].append(word)
    
        return key_dict
    
    def check(self, question):
        """Search in the question if there exist a signature phrase in the question and will return the intent if exist or false if not
        """       
        
        key_dict = self.read_signature_data_from_file()

        # Load library (can put outside to improve performance) 
        nlp = spacy.load("en_core_web_sm")
        
        # Initialize Phrase matcher model
        matcher = PhraseMatcher(nlp.vocab,  attr="LOWER")
        
        # Initialize matching phrase
        for key in list(key_dict.keys()):
            patterns = [nlp.make_doc(text) for text in key_dict[key]]
            matcher.add(key, patterns)
        
        doc = nlp(question)
        matches = matcher(doc)
        if len(matches) == 1:
            return nlp.vocab.strings[matches[0][0]]
        elif len(matches) >= 1 & all(x == matches[0][0] for x in matches):
            return nlp.vocab.strings[matches[0][0]]
        else: 
            return False