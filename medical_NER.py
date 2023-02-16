# import pandas as pd
# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt')
#
# df = pd.read_csv("NLP_models/NER_Data/drugs_side_effects_drugs_com.csv")
# drug_names = set(df["drug_name"])
# drug_names = [word_tokenize(name) for name in drug_names]
# drugs = []
# for name_list in drug_names:
#     if "/" in name_list:
#         drugs.append(name_list[0].lower())
#         drugs.append(name_list[2].lower())
#     else:
#         drugs.append(name_list[0].lower())
#
# print(df.columns)
#
# medical_conditions = df["medical_conditions"]

import spacy

nlp_ner = spacy.load("model-best")
roberta_nlp = spacy.load("en_core_web_trf")
# print_entities(roberta_nlp, text)

# doc = nlp_ner(
    # "While bismuth compounds (Pepto-Bismol) decreased the number of bowel movements in those with travelers' diarrhea, they do not decrease the length of illness.[91] Anti-motility agents like loperamide are also effective at reducing the number of stools but not the duration of disease.[8] These agents should be used only if bloody diarrhea is not present.")

colors = {"PATHOGEN": "#F67DE3", "MEDICINE": "#7DF6D9", "MEDICALCONDITION": "#a6e22d"}
options = {"colors": colors}

# for ent in doc.ents:
    # print(ent.text, ent.start_char, ent.end_char, ent.label_)


def getEntities(txt, model):
    if model=="custom":
        doc = nlp_ner(txt)
        entities = []
        for ent in doc.ents:
            entity = ent.text
            label = ent.label_
            entities.append((entity.lower(), label))

        return entities
    else:
        doc = roberta_nlp(txt)
        products = []
        quantity = []
        for ent in doc.ents:
            entity = ent.text
            label = ent.label_
            if label=="PRODUCT":
                products.append([e for e in entity.split()][0].lower())
            if label=="QUANTITY":
                quantity.append(entity.lower())

    return products, quantity

text = "DESCRIPTION TYLENOL ® with Codeine is supplied in tablet form for oral administration. Acetaminophen, 4'-hydroxyacetanilide, a slightly bitter, white, odorless, crystalline powder, is a non-opiate, non-salicylate analgesic and antipyretic. It has the following structural formula: C 8 H 9 NO 2 M.W. 151.16 Codeine phosphate, 7,8-didehydro-4, 5α-epoxy-3-methoxy-17-methylmorphinan-6α-ol phosphate (1:1) (salt) hemihydrate, a white crystalline powder, is a narcotic analgesic and antitussive. It has the following structural formula: C 18 H 21 NO 3 ∙H 3 PO 4 ∙1/2 H 2 O M.W. 406.37 Each Tylenol with Codeine No. 3 tablet, USP (300 mg/30 mg) contains: Acetaminophen 300 mg Codeine Phosphate 30 mg Each Tylenol with Codeine No. 4 tablet, USP (300 mg/60 mg) contains: Acetaminophen 300 mg Codeine Phosphate 60 mg In addition, each tablet contains the following inactive ingredients: TYLENOL ® with Codeine No. 3 contains powdered cellulose, magnesium stearate, sodium metabisulfite See WARNINGS , pregelatinized starch (corn), and modified starch (corn). TYLENOL ® with Codeine No. 4 contains powdered cellulose, magnesium stearate, sodium metabisulfite , pregelatinized starch (corn), and corn starch. Chemical Structure Chemical Structure"
print(getEntities(text, "custom"))

