# bad_test_api.py
import json

import requests

url = "http://localhost:8000/items/"

item_data: dict[str, str | float] = {
    # Here we exclude the "name" field to simulate a bad request. It
    # is required by the API schema.
    # "name": "Sample Item",
    "description": "This is a sample item.",
    "price": 19.99,
    "tax": 1.5
}

response = requests.post(url, json=item_data)
print("Status Code:", response.status_code)
print("Response JSON:")
print(json.dumps(response.json(), indent=2))
