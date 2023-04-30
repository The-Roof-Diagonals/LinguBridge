from libs.chatgpt import gpt
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import os
from dotenv import load_dotenv
import requests 
from sklearn.feature_extraction.text import TfidfVectorizer
load_dotenv()
DEEPL_ENDPOINT= "api-free.deepl.com"
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
import en_core_web_md
nlp = en_core_web_md.load()
nlp = spacy.load("en_core_web_md")


def translate_text(to_lang, text):
    result = requests.get( 
        f"https://api-free.deepl.com/v2/translate", 
        params={ 
            "auth_key": DEEPL_API_KEY, 
            "target_lang": to_lang, 
            "text": text, 
    })
    print(result.text)
    return result.json()["translations"][0]["text"]

    
def spacy_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def tfidf_sicmilarity(text1, text2):
    documents = [text1, text2]
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity.toarray()[0][1]

report= '''
Reason and solution of the problem / accomplished work
I met with the customer, Mr. Dennis Huff, who is the maintenance supervisor, to conduct an entrance interview. He told
me that the machine had been down for about an hour so I could inspect some items before it resumed production of B /
E double wall. I checked the lower corrugating roll and found its number W-76702, but the other roll had a lot of build up
that obscured its number. I took NCR's to measure the parallelism of the corrugating rolls. The lineal counter showed
66,781,034 million lineal feet. I also looked at the roll condition briefly. I talked to the maintenance department about
what they had done in the last two weeks to fix some issues with the machine. They said they had to adjust the
corrugating roll parallel several times and that the roll slot wear was misaligned at ambient temperature. I checked the
alignment of the corrugating rolls at heated condition and found a clear misalignment. The wear pattern on the lower
corrugating roll was shifted by about two millimeters. I arranged for the machine to be cooled off for the weekly
PM maintenance. I examined the corrugating rolls and saw significant plating loss on the tips and root radius of the rolls.
The NCR's showed larger impressions than expected for the lineal footage on the counters. There was also a noticeable
average paper width wear pattern on the rolls. When I applied 90 bar to the rolls, I saw that there was no engagement
on both sides of the width for about 10 inches, centered 18 inches from the ends of the rolls. The shifting of the
corrugating rolls was evident in the NCR's marks. The second resonance samples showed malformed flutes.'''






def get_similarity_scores(original_text, translated_text, language_original):
    print("Language original:")
    print(language_original)
    print("Original text:")
    print(original_text)
    print("Translated text:")
    print(translated_text)
    # THIS translated_text_back_to_original_language = translate_text(language_original, translated_text)
    translated_text_back_to_original_language = translate_text_azure("", language_original, translated_text)
    #print("Spacy similarity (NLP-model): " + str(spacy_similarity(report, translated_text_back_to_original_language)) + "%\n")
    #print("TFIDF similarity (NLP-model): " + str(tfidf_similarity(report, translated_text_back_to_original_language)) + "%\n")
    similarity = gpt("Rate the similarity in the content (ignore the language differences) of the two texts on a scale from 0 to 100 and only return the number!:\n Text 1:\n\"" + 
                     original_text + "\"\n\nText 2:\n \"" + translated_text +"\"")
    #print(f"Similarity between the content of the translated text and the original (LLM-model):\n{similarity}%")


    return {
        "spacy": spacy_similarity(original_text.strip().replace("\n", " "), translated_text_back_to_original_language.strip().replace("\n", " ")),
        "tfidf": tfidf_similarity(original_text.strip().replace("\n", " "), translated_text_back_to_original_language.strip().replace("\n", " ")),
        "gpt": similarity
    }


import uuid
import requests
import json

def translate_text_azure(from_lan, target_lan, text):
    key = "fd452c00f8c14bee9bc61765053e1425"
    endpoint = "https://api.cognitive.microsofttranslator.com/"

    location = "westeurope"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_lan,
        'to': [target_lan]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return response[0]["translations"][0]["text"]

#translate_text_azure("", "de", "I would really like to drive your car around the block a few times!")