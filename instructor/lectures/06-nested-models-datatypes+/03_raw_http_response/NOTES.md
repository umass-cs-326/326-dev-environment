## 3. RAW HTTP RESPONSE

When the server processes this request, it sends back a raw HTTP response, which might look like this:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 85  

{
    "id": 1,
    "name": "Sample Item",
    "description": "This is a sample item.",
    "price": 19.99,
    "tax": 1.5
}
```

This response consists of:

- **Status Line**: `HTTP/1.1 201 Created` indicates that the request was successful and a new resource was created.
- **Headers**: Similar to the request, these provide metadata about the response.
- **Body**: This contains the data being sent back to the client, in this case, a JSON object representing the newly created item with its assigned ID.
- **Status Code**: The `201 Created` status code indicates that the request has been fulfilled and has resulted in one or more new resources being created.
- **Content-Type**: The `Content-Type` header specifies the media type of the resource. In this case, it indicates that the response body is in JSON format.
- **Content-Length**: The `Content-Length` header indicates the size of the response body in bytes.
