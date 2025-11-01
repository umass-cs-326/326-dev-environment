## 2. RAW HTTP REQUEST

When we send a request to an API, we are sending a raw HTTP request. This is what the request looks like when it is sent over the internet.

```http
POST /items/ HTTP/1.1
Host: example.com
Content-Type: application/json
Content-Length: 123 

{
    "name": "Sample Item",
    "description": "This is a sample item.",
    "price": 19.99,
    "tax": 1.5
}
```

**NOTE: the request is sent as plain text over the internet.**

This request consists of:

- **Request Line**: `POST /items/ HTTP/1.1` indicates that we are making a POST request to the `/items/` endpoint using HTTP version 1.1.
- **Headers**: These provide metadata about the request. For example, `Content-Type: application/json` indicates that the body of the request is in JSON format.
- **Body**: (Optional) This contains the actual data being sent to the server, in this case, a JSON object representing an item.
