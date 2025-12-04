import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
ENDPOINT = os.getenv("API_ENDPOINT")

#THIS WORKSSSS
def test_authorize_token():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "accept": "*/*"
    }

    response = requests.get(ENDPOINT, headers=headers)

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

test_authorize_token()

def test_rates():
    url = "https://api.shipwise.com/api/v1/Rate"

    payload = {
        "clientId": 307439,
        "profileId": 7001213,
        "ratingOptionID": "Standard Service Group",
        "to": {
            "name": "John Doe",
            "address1": "14950 SW Barrows Rd",
            "city": "Beaverton",
            "postalCode": "97007",
            "state": "OR",
            "countryCode": "US",
            "countryName": "United States"
        },
        "from": {
            "name": "Jane Smith",
            "address1": "1224 Exposition Way",
            "city": "San Diego",
            "postalCode": "92154",
            "state": "CA",
            "countryCode": "US",
            "countryName": "United States"
        },
        "packages": [
            {
                "totalWeight": 5,
                "packaging": {
                    "length": 10,
                    "width": 5,
                    "height": 8,
                    "cost": 0.1
                },
                "items": [
                    {
                        "marketSku": "SKU12345",
                        "marketTitle": "Sample Item",
                        "orderedQty": 1,
                        "unitPrice": 20.0,
                        "giftMsg": "Happy Birthday!",
                        "giftNotes": "Enjoy your gift!",
                        "weight": 5,
                        "originCountry": "United States",
                        "harmCode": "4901.04",
                        "customsDescription": "Books",
                        "customsDeclaredValue": 20.0,
                        "upc": "012345678905",
                        "length": 10,
                        "width": 5,
                        "height": 8
                    }
                ],
                "value": 10
            }
        ],
        "testMode": "true"
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "accept": "text/plain*"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)