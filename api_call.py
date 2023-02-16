import requests
from NLP_models.summarizer_functions import *

response = requests.get("https://api.fda.gov/drug/label.json?search=description:tylenol&limit=3")
json_res = response.json()

print(json_res["results"][2].keys())


def getDescription(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=2"
    response = requests.get(url).json()
    try:
        return response["results"][0]["description"][0]
    except:
        return ""

def getAdverseReactions(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=2"
    response = requests.get(url).json()
    try:
        return response["results"][0]["adverse_reactions"][0]
    except:
        return ""


def getUsage(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=1"
    response = requests.get(url).json()
    try:
        return response["results"][0]["indications_and_usage"][0]
    except:
        return ""


def getWarnings(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=1"
    response = requests.get(url).json()
    try:
        return response["results"][0]["warnings"][0]
    except:
        return ""


def getPrecautions(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=1"
    response = requests.get(url).json()

    return response["results"][0]["precautions"][0]


def getInfo(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=1"
    response = requests.get(url).json()
    try:
        return response["results"][0]["information_for_patients"][0]
    except:
        return ""


def getSummary(name, n):  #name: brand name
    final_str = ""

    info = getInfo(name)
    if info != '':
        final_str += "General Information: \n"
        final_str += bert_extractive(info, n) + "\n\n"

    des = getDescription(name)
    if des != '':
        final_str += "Description: \n"
        final_str += bert_extractive(des, n) + "\n\n"

    use = getUsage(name)
    if use != '':
        final_str += "Usage: \n"
        final_str += bert_extractive(use, n) + "\n\n"

    adverse = getAdverseReactions(name)
    if adverse != '':
        final_str += "Adverse Reaction: \n"
        final_str += bert_extractive(adverse, n) + "\n\n"

    pre = getPrecautions(name)
    if pre != '':
        final_str += "Precautions: \n"
        final_str += bert_extractive(pre, n) + "\n\n"

    warn = getWarnings(name)
    if warn != '':
        final_str += "Warnings: \n"
        final_str += bert_extractive(warn, n) + "\n\n"

# print(getDescription("tylenol"))
