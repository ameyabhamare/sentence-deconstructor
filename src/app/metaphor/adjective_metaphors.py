import spacy
import sys
import os
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

if __name__  not in ["__main__","adjective_metaphors"]:
    sys.path.append("..")
    from app.metaphor.MetaphorUtil import MetaphorUtil
else:
    from MetaphorUtil import MetaphorUtil

nlp = spacy.load("en_core_web_sm")

class AdjectiveMetaphor(MetaphorUtil):

    def __init__(self, text='', sp_w = 0.00, wp_w = 0.00, threshold = 0.00):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        self.sim_scores = []
        # self.paragraph = paragraph
        self.spacy_weight = sp_w
        self.wupalmer_weight = wp_w
        self.threshold = threshold

    def compare_categories(self, adj, object, adj_syn, obj_syn):
        metaphor = False

        cat_adj = self.extract_lexical_categories(adj_syn)
        cat_obj = self.extract_lexical_categories(obj_syn)

        common_categories = cat_adj.intersection(cat_obj)
        if len(common_categories) == 0:
            message = "\nNo overlap => {0} and {1} are METAPHORICAL".format(adj, object)
            metaphor = True
        else:
            main_cat_adj = self.find_main_category(adj, cat_adj, key="adj")
            main_cat_object = self.find_main_category(object, cat_obj, key="noun")

            if main_cat_adj != main_cat_object: # Different main categories
                message = "\nMain categories are different => {0} and {1} are METAPHORICAL".format(adj, object)
                metaphor = True
            else:
                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)
    
    def is_adj_metaphor(self, noun, adjective):
        adj_syn = self.return_synsets(adjective)
        noun_syn = self.return_synsets(noun)
        
        index_adj = self.index_synset(adj_syn, adjective)
        index_noun = self.index_synset(noun_syn, noun)

        sim_result = self.spacy_similarity(adjective, noun)
        print("Similarity:", sim_result)

        # if index_adj == -1 or index_noun == -1:
        #     if sim_result > 0.4:
        #         message = "Similarity score found to be high at {0}".format(sim_result)
        #         metaphor = "Maybe"
        #     else:
        #         message = "Metaphor due to low similarity score of {0}".format(sim_result)
        #         metaphor = True

        #     # Can't proceed further because comparison of categories needs synsets again :( => can only check with Spacy)

        # else:
        #     wup_result = self.wu_palmer_similarity(adj_syn, index_adj, noun_syn, index_noun)[0]
        #     sim_result = self.spacy_similarity(adjective, noun)

        #     sim_score = max(wup_result, sim_result)
        #     self.sim_scores.append(sim_score)

        #     if sim_score < 0.3:
        #         metaphor = True
        #         message = "Metaphor due to low similarity score of {0}".format(sim_score)
        #     else:
        #         message, metaphor = self.compare_categories(adjective, noun, adj_syn, noun_syn)

        # return (message, metaphor)
    
    def adj_metaphor_util(self, doc, code=0):
        
        # Find all adj-noun pairs
        noun_adj_pairs = {}
        for chunk in doc.noun_chunks:
            adj = []
            noun = ""
            for tok in chunk:
                if tok.pos_ == "NOUN":
                    noun = tok.text
                if tok.pos_ == "ADJ" or tok.pos_ == "CCONJ":
                    adj.append(tok.text)
            if noun:
                noun_adj_pairs.update({noun:adj})
        
        for noun in noun_adj_pairs:
            for adjective in noun_adj_pairs[noun]:

                    if code == 1: # FINDING OPTIMAL WEIGHTS
                        final_score = self.return_similarity_score(noun, adjective, code) 
                        if final_score > self.threshold:
                            return ("N", final_score)
                        else:
                            return ("Y", final_score)
            
                    elif code == 2: # ADD SIM TO CSV
                        return self.return_similarity_score(noun, adjective, code = 2)
                    
                    else:
                        similarity = self.return_similarity_score(noun, adjective)

                        if similarity < self.threshold:
                            self.metaphors.append(("{0} and {1} could be metaphorical as similarity score is low".format(noun, adjective),"Y"))
                        else:
                            self.metaphors.append(("{0} and {1} are probably not metaphorical as similarity score is high".format(noun, adjective),"N"))
    
    def add_individual_scores(self):
        spacy_scores = []
        wup_scores = []
       
        with open("am_data/AM_data.txt","r") as file:
            data = list(map(lambda x: x.strip("\n"),file.readlines()))
        
        for text in data:
          doc = nlp(text)
          spac, wup = self.verb_metaphor_util(doc, code = 2)

        spacy_scores.append(spac)
        wup_scores.append(wup)

        # print(spacy_scores)
        data = {"Text": data, "Spacy":spacy_scores, "WUP": wup_scores}
        df = pd.DataFrame(data)

        df.to_csv("am_data/AM_similarities.csv")
    
    def train(self,data, true_values):

        # train, test = train_test_split()
        # print(data)
        max_acc = 0.00
        best_threshold = 0.00
        optimal_weights = (0.00,0.00)

        new_threshold = 0.00

        for spw in np.arange(0,1,0.001):
            wpw = 1 - spw
            self.threshold = new_threshold, 
            self.spacy_weight =spw
            self.wupalmer_weight =wpw

            predictions = []
            scores = []

            for text in data:
                # print()
                # print("---------------------------------------------------")
                # print(text)
                # self.text = text
                doc = nlp(text)
                self.dependencies = {}
                pred,score = self.adj_metaphor_util(doc, code=1)

                predictions.append(pred)
                scores.append(score)

            new_threshold = sum(scores)/len(scores)
            
            acc = self.find_accuracy(predictions, true_values)
            if acc > max_acc:
                max_acc = acc
                best_threshold = new_threshold
                optimal_weights = (spw, wpw)
        
        print("Maximum Accuracy:", max_acc)
        print("Optimal Threshold:", best_threshold)
        print("Optimal Weights:", optimal_weights)

        self.threshold = best_threshold
        self.spacy_weight, self.wupalmer_weight = optimal_weights

    def test(self, data, true_values):
        scores = []
        predictions = []

        for text in data:
                # print()
                # print("---------------------------------------------------")
                # print(text)
                # self.text = text
                doc = nlp(text)
                self.dependencies = {}
                pred,score = self.adj_metaphor_util(doc, code=1)

                predictions.append(pred)
                scores.append(score)

        print("Weights - Spacy: {0} and Wu-Palmer: {1}".format(self.spacy_weight, self.wupalmer_weight))
        print("Threshold:",self.threshold)
        print("Test Accuracy:", self.find_accuracy(predictions, true_values))

    def detect_adj_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.adj_metaphor_util(doc)
        return self.metaphors


if __name__ == "__main__":
    start = time.time()
    print("Start Time:", start)
    print()

    with open("vm_data/VM_data.txt","r") as file:
        data = list(map(lambda x: x.strip("\n"),file.readlines()))

    
    AM_Trial = AdjectiveMetaphor()
    AM_Trial.add_individual_scores()
    
    # df = pd.read_csv("am_data/AM_similarities.csv")
    # # print(df['Metaphor'])

    # train_X, test_X, train_Y, test_Y = train_test_split(df["Text"],df['Metaphor'], stratify=df["Metaphor"], shuffle=True, test_size=0.10, random_state=42)

    # # print(train_X, train_Y)

    # AM_Trial = AdjectiveMetaphor()
    # AM_Trial.train(train_X, train_Y)
    # print("\n\n")
    # AM_Trial.test(test_X, test_Y)
    # # find_optimal_weights()

    # print()
    # end = time.time()
    # print("End Time:", end)
    # print("Time taken:{0} minutes", (end - start)/60)_name__ == "__main__":
    
    
    # OLD CODE
    # texts = ["The old woman had a cold heart."]
    # AM_Trial = AdjectiveMetaphor(None)

    # for text in texts:
    #     AM_Trial.text = text
    #     AM_Trial.detect_adj_metaphor()
    #     print(AM_Trial.metaphors)