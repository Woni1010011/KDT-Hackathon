from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import requests
import uuid
import time
import json, os
import re

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
secret_file = os.path.join(BASE_DIR, "secrets.json")  # secrets.json 파일 위치를 명시


with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

api_url = 'https://8f3i43jr3e.apigw.ntruss.com/custom/v1/25689/280f4c02524b72e8e5958601c32c4eb2239d88e34555559f7056c7268db0648c/general'
secret_key = get_secret("CLOVA_OCR_KEY")

def tempFunction (image) :
    request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(image,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

    result = response.json()
    with open('result.json', 'w', encoding='utf-8') as make_file:
        json.dump(result, make_file, indent="\t")


    text = ""

    for field in result['images'][0]['fields']:
        if 'P' in field['inferText'] :
            start_index = field['inferText'].find("P") + 1
            end_index = field['inferText'].find("/")

            if start_index >= 0 and end_index >= 0:
                result_string = field['inferText'][start_index:end_index]
                text += result_string + "\n"
            else:
                match = re.search(r'P(.*?)\(', field['inferText'])
                if match:
                    result_string = match.group(1)
                    text += result_string + "\n"
                else:
                    pass

    print(text)
    
    return text

image = os.path.join(BASE_DIR, "nh_image05.jpg")
tempFunction(image)
