from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

def imagetotext(filename):
    # process image
    endpointlul = "https://ronwonk.cognitiveservices.azure.com/"
    key1 = "5418d7e123b644d5a8b45b44978880e2"
    key2 = "01ef10d1dd5a4709b9227ef4fcc0d460"

    

    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = key1
    endpoint = endpointlul

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    '''
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriting style text (not shown).
    '''
    print("===== Read File - remote =====")
    # Get an image with text
    #read_image_url = "https://cdn.shopify.com/s/files/1/0275/6457/2777/files/Penwritten_2048x.jpg?v=1614384788"
    f = open(filename, "rb")
    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(f,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    text = ""
    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
                text += line.text + "\n"
    print()
    '''
    END - Read File - remote
    '''

    print("End of Computer Vision quickstart.")
    return text