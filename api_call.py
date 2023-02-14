import requests
# from gensim.summarization.summarizer import summarize
# from gensim.summarization import keywords
# from NLP_models.summarizer_nltk import *
import json

response = requests.get("https://api.fda.gov/drug/label.json?search=description:tylenol&limit=2")
json_res = response.json()

# print(json_res["error"])


def getDescription(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=description:{drug_name}&limit=2"
    response = requests.get(url).json()
    try:
        return response["results"][0]["description"][0]
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

# def getSummary(name):
#
#     final_str = ""
#
#     info = getInfo(name)
#     if


# print(getDescription("tylenol"))
