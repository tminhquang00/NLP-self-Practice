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

import os
import pandas as pd
from datetime import datetime
import csv

class Logger:
    
    def __init__(self, path_to_log_file) -> None:

        self.path_to_log_file = path_to_log_file

        self.create_log_file()
        

    def create_log_file(self):
        """Create log file for chatbot, this function should be call once when chatbot start 
            - The function will check if the log folder, if log file hasn't been created, this function 
            will create a new log file.       
            - Output file format will be: chatbot_log.xlsx             
        """
        
        headers = ["session_id","sent_time","raw_input","preprocessed_input","classified_intent",
                "classification_score","chatbot_response","sentence_similarity_score",
                "correspondance_question","id"]

        # Create empty dataframe with predefine headers
        df = pd.DataFrame(columns = headers) 

        # Create log file if not exist
        if(os.path.exists(self.path_to_log_file) == False):
            df.to_csv(self.path_to_log_file, index=False)

    def write_log(self, session_id, raw_input, preprocessed_input, classified_intent, classification_score,
        chatbot_response, sentence_similarity_score, correspondance_question, id):
        """Save log data        
        Args:
            session_id          : str                     User ID
            raw_input           : str                     User Input
            preprocessed_input  : str                     Preprocessed user input
            classified_intent   : list of str             Top n intents
            classification_score: list of float           Confident core of top n intents
            chatbot_response    : list of str             Response of the chatbot
            sentence_similarity_score: list of float      Cosine similarity of the response
            id                  : str                     Unique ID of question
        """
        now = datetime.now()        
        current_time = now.strftime("%d:%m:%Y"+"_"+"%H:%M:%S")

        # Aggregate data into a list
        data = [
            session_id,                 current_time,
            raw_input,                  preprocessed_input,
            classified_intent,          classification_score,
            chatbot_response,           sentence_similarity_score,
            correspondance_question,    id
        ]

        # Export the log data into file via outstream
        with open(self.path_to_log_file, "a",encoding="utf-8", newline='') as f:
            writer = csv.writer(f, delimiter=",") 
            writer.writerow(data)
