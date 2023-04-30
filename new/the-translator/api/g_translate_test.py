import six
from google.cloud import translate_v2 as translate

def translate_text_google(target_language, text):
    key = "AIzaSyAxb9Sqq0XDlWntlXM98n52XsCOO5xwr5k"
    translate_client = translate.Client()
    translate_client._credentials = ""

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]


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
        'text': 'I would really like to drive your car around the block a few times!'
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return response[0]["translations"][0]["text"]

translate_text_azure("", "de", "I would really like to drive your car around the block a few times!")