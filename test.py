import os
import requests
from api_call import getDescription

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

from summarizer import Summarizer, TransformerSummarizer

text1 = getDescription("tylenol")
#
# model = Summarizer()
# result = model(text1, num_sentences=3, min_length=60)
# full = ''.join(result)

GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
full = ''.join(GPT2_model(text1, min_length=60))
print(full)
print(text1)
