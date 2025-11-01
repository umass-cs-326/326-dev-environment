from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Tell FastAPI where templates and static files live
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user: dict[str, Request | dict[str, str | int | list[str]]] = {
        "request": request,
        "user": {
            "name": "Daniel Brown",
            "age": 20,
            "hobbies": [
                "fishing", "scuba", "food"
            ]
        },
    }
    return templates.TemplateResponse("index.html", user)

# FastAPI route


@app.get("/products")
async def products(request: Request):
    products = [  # type: ignore
        {"name": "laptop", "price": 999.99,
         "description": "A high-performance laptop with amazing features and long battery life"},
        {"name": "mouse", "price": 25.5,
         "description": "Ergonomic wireless mouse"},
    ]
    return templates.TemplateResponse("products.html", {"request": request, "products": products})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
