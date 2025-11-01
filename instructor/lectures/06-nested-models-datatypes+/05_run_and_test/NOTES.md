## 5. Run and Test the Application

Now that the FastAPI application is set up, you can run it and test the endpoint:

```bash
uvicorn main:app --reload
```

Now let us write a Python script to test our API endpoint.

```python
# test_api.py
import json

import requests

url = "http://localhost:8000/items/"

item_data: dict[str, str | float] = {
    "name": "Sample Item",
    "description": "This is a sample item.",
    "price": 19.99,
    "tax": 1.5
}

response = requests.post(url, json=item_data)
print("Status Code:", response.status_code)
print("Response JSON:")
print(json.dumps(response.json(), indent=2))
```

Run the test script:

```bash
python test_api.py
```
