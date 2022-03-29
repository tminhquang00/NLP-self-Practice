
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
# pip install thefuzz[speedup]
from thefuzz import fuzz
from thefuzz import process

import pandas as pd
import numpy as np

class FuzzyMatcher:
    
    def __init__(self, data_path = 'data/greeting_sample.csv'):
        self.data_path = data_path
        self.questions = list()
        self.responses = list()
       
    
    def read_greeting_data_from_file(self):
        """ Read data from csv             
        """
        data = pd.read_csv(self.data_path,encoding = 'utf-8')
        questions = data['question'].tolist()
        responses = data['response'].tolist()
        return questions, responses
    
    
    def get_the_best_match(self, input_question):
        '''
        Get the most simlar question from the greeting list
        
        '''
        self.questions, self.responses = self.read_greeting_data_from_file()

        best_match, score = process.extractOne(input_question, self.questions, scorer=fuzz.ratio)
        if score > 80:
            return best_match
        
        else:
            best_match, score = process.extractOne(input_question, self.questions, scorer=fuzz.token_sort_ratio)
            if score > 90:
                return best_match
            return False
        
        
    def get_response(self, input_question):
        '''
        Get the response based on question
        
        '''

        for q, r in zip(self.questions, self.responses):
            if q == input_question:
                return r
        return False