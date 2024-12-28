from dotenv import load_dotenv
import os
import requests
import hashlib
import hmac


load_dotenv()

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["SECRET_KEY"]

def boilerplate(params, endpoint):
    BASE_URL = 'https://api.binance.com'

    # Create the signature using HMAC-SHA256
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Add the signature to the parameters
    params['signature'] = signature

    # Define the headers with API key
    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    # Send the GET request
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)

    # Check response status and print the result
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return Exception(f"Error: {response.status_code}, {response.text}")

def boilerplate1(params, endpoint):
    BASE_URL = 'https://api.binance.com'

    # Define the headers with API key
    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    # Send the GET request
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)

    # Check response status and print the result
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return Exception(f"Error: {response.status_code}, {response.text}")