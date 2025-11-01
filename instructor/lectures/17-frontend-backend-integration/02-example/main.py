from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Global counter variable
click_count = 0


@app.get("/", response_class=HTMLResponse)
async def serve_html(request: Request):
    """Serve the example.html file with Jinja2 templating"""
    return templates.TemplateResponse(
        "example.html",
        {"request": request, "initial_count": click_count}
    )


@app.get("/click", response_class=HTMLResponse)
async def handle_click():
    """Handle click events and return updated counter"""
    global click_count
    click_count += 1
    return f"<p>Click count: {click_count}</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
