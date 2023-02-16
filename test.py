import os
import requests

import medical_NER
# from api_call import getDescription

# good_brands = []
#
# name_list = os.listdir(r"C:\Users\sarin\Documents\Science Fair Data\packaging_images")
# for name in name_list:
#     name_list = [x for x in name.split()]
#     url = f"https://api.fda.gov/drug/label.json?search=description:{name_list[0].lower()}&limit=2"
#     response = requests.get(url).json()
#     try:
#         res = response["results"]
#         good_brands.append(name)
#     except:
#         continue
#
# print(good_brands)
# print(len(good_brands))

# from gensim.summarization.summarizer import summarize
# from gensim.summarization import keywords

# from summarizer import Summarizer, TransformerSummarizer
#
# text1 = getDescription("tylenol")
# #
# # model = Summarizer()
# # result = model(text1, num_sentences=3, min_length=60)
# # full = ''.join(result)
#
# GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
# full = ''.join(GPT2_model(text1, min_length=60))
# print(full)
# print(text1)
from medical_NER import getEntities

text = "While bismuth compounds (Pepto-Bismol) decreased the number of bowel movements in those with travelers' diarrhea, they do not decrease the length of illness.[91] Anti-motility agents like loperamide are also effective at reducing the number of stools but not the duration of disease.[8] These agents should be used only if bloody diarrhea is not present."

#

#make new df

import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

df = pd.read_csv("drugs_side_effects_drugs_com.csv")
med_cond_1 = list(df["medical_condition"])
med_cond =[]
for i in med_cond_1:
    name = word_tokenize(i)
    med_cond.append(name[0].lower())
url = list(df["medical_condition_url"])

new_df = pd.DataFrame(list(zip(med_cond, url)))
new_df.columns=["medical_condition", "url"]
new_df = new_df.drop_duplicates().reset_index(drop=True)
new_df.to_csv("medical_condition_urls.csv")
print(new_df)
