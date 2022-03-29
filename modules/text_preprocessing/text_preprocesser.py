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
import re
import nltk

class TextPreprocesser:

    def __init__(self, path_to_abbrev_word_list) -> None:
        
        self.abbreviations_list = self.get_abbre_words_list(path_to_abbrev_word_list)
   
    def get_abbre_words_list(self, path_to_data_file):
        """ Pre-process input texts with tokenization
        Args:
            path_to_data_file: str
                Path to the abbreviation data file.
        Returns:
            List of tuples 
                words and list of abbreviations words of these words
        """
        # Read dataframe from csv   
        df_addbre = pd.read_csv(path_to_data_file, encoding = "utf-8")

        # Extract questions, answer and intent labels in 3 lists
        words = df_addbre['Words'].tolist()
        list_abbre_words   = df_addbre['Abbreviations'].tolist()

        # Construct the list of abbreviation terms for mapping
        list_abbre_words_processed = []
        for (w,a) in zip(words, list_abbre_words):
            abbre_words = a.strip().split(',')
            abbre_of_w = []
            for word in abbre_words:                
                word = re.sub(r'[^\w\s]', '', str(word).lower().strip())
                if(len(word) > 0):
                    abbre_of_w.append(word)
            list_abbre_words_processed.append((w, abbre_of_w))
        return list_abbre_words_processed

    def preprocess_a_sentence_change_abbre(self, text, remove_stopword=False, 
        has_stemming=False, has_lemmatization=True):
        """ Pre-process input texts with tokenization
        Args:
            text:              str
                the input text to preprocess (e.g., question, answer)
            remove_stopword:   bool
                the functional flag to control stopword removal
            has_stemming:      bool
                the functional flag to control stemming (e.g., -ing, -ly, ...)
            has_lemmatization: bool
                the functional flag to control lemmatization (e.g. plural to singular)
        Returns:
            str
                the text after preprocessing
        """
        
        # Convert to lowercase, Remove punctuations
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

        # Tokenize the sentence
        lst_tokens = text.split()

        # Stemming (remove -ing, -ly, ...)
        if has_stemming == True:
            stemmer = nltk.stem.porter.PorterStemmer()
            # stemmer2 = nltk.stem.snowball.SnowballStemmer("english")
            # stemmer3 = nltk.stem.LancasterStemmer()        
            lst_tokens = [stemmer.stem(word) for word in lst_tokens]
        text = ' '.join(map(str,lst_tokens))
        
        # Replace the abbreviation terms
        if len(self.abbreviations_list) > 0:            
            for (general_word, list_abbre_of_w) in self.abbreviations_list:
                for abbre_word in list_abbre_of_w:
                    if(len(abbre_word) > 0):
                        text = text.replace(abbre_word, general_word)          

        # Remove stopwords
        lst_stopwords = nltk.corpus.stopwords.words("english")
        lst_tokens = text.split()
        if remove_stopword:
            lst_tokens = [word for word in lst_tokens if word not in lst_stopwords]
                    
        # Lemmatisation (remove plural, change into singular)
        if has_lemmatization == True:
            lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
            lst_tokens = [lemmatizer.lemmatize(word) for word in lst_tokens]
            
        # Join tokens and Return a string
        return " ".join(lst_tokens)

    def preprocess_a_sentence(self, text, remove_stopword=False, has_stemming = False, has_lemmatization = True):
        """ Pre-process input texts without tokenization
        Args:
            text:              str
                the input text to preprocess (e.g., question, answer)
            remove_stopword:   bool
                the functional flag to control stopword removal
            has_stemming:      bool
                the functional flag to control stemming (e.g., -ing, -ly, ...)
            has_lemmatization: bool
                the functional flag to control lemmatization (e.g. plural to singular)
            
        Returns:
            str
                the text after preprocessing
        """
        
        # Convert to lowercase, Remove punctuations
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
                
        # Tokenize the sentence
        lst_tokens = text.split()
        
        # Remove stopwords
        lst_stopwords = nltk.corpus.stopwords.words("english")
        if remove_stopword:
            lst_tokens = [word for word in lst_tokens if word not in lst_stopwords]
                    
        # Stemming (remove -ing, -ly, ...)
        if has_stemming == True:
            stemmer = nltk.stem.porter.PorterStemmer()
            # stemmer2 = nltk.stem.snowball.SnowballStemmer("english")
            # stemmer3 = nltk.stem.LancasterStemmer()        
            lst_tokens = [stemmer.stem(word) for word in lst_tokens]
                    
        # Lemmatisation (remove plural, change into singular)
        if has_lemmatization == True:
            lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
            lst_tokens = [lemmatizer.lemmatize(word) for word in lst_tokens]
                
        # Join tokens and Return a string
        return " ".join(lst_tokens)

    def preprocess_sentence_list(self, sentence_lst):
        """
        Args:
            sentence_lst:       List[str]
                a list of sentences that needed to preprocess
        Returns:
            List[str]
                a list of preprocessed sentences
        """

        # Preprocess each sentence iteratively one-by-one
        preprocessed_lst = []
        for sentence in sentence_lst:
            preprocessed_lst.append(
                self.preprocess_a_sentence(sentence)
            )

        return  preprocessed_lst

