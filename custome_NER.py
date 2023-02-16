import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

df = pd.read_csv("NLP_models/NER_Data/drugs_side_effects_drugs_com.csv")
drug_names = set(df["drug_name"])
drug_names = [word_tokenize(name) for name in drug_names]
drugs = []
for name_list in drug_names:
    if "/" in name_list:
        drugs.append(name_list[0].lower())
        drugs.append(name_list[2].lower())
    else:
        drugs.append(name_list[0].lower())

print(df.columns)

medical_conditions = df["medical_conditions"]