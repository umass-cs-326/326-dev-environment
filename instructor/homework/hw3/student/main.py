# main.py
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from starlette.middleware.sessions import SessionMiddleware
from models import User, Book, create_db_and_tables, get_session
from auth import hash_password, verify_password, get_current_user

app = FastAPI()

# Add session middleware for authentication
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to login page"""
    return RedirectResponse(url="/login")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Show registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Handle user registration"""
    # TODO: Check if user already exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    # TODO: Create new user with hashed password
    hashed_pw = hash_password(password)
    new_user = User(name=name, email=email, password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # TODO: Set session and redirect to dashboard
    request.session["user_id"] = new_user.id
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Handle user login"""
    # TODO: Find user by email
    user = session.exec(select(User).where(User.email == email)).first()
    
    # TODO: Verify password
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"}
        )
    
    # TODO: Set session and redirect
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: Session = Depends(get_session)
):
    """Show user dashboard with books"""
    # TODO: Get current user (will raise 401 if not authenticated)
    try:
        user = get_current_user(request, session)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    # TODO: Get user's books
    books = session.exec(select(Book).where(Book.user_id == user.id)).all()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "books": books}
    )

@app.post("/books")
async def create_book(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    session: Session = Depends(get_session)
):
    """Create a new book (HTMX endpoint)"""
    try:
        user = get_current_user(request, session)
    except HTTPException:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    # TODO: Create new book
    new_book = Book(title=title, author=author, user_id=user.id)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    
    # TODO: Return fragment with new book
    return templates.TemplateResponse(
        "fragments/book_item.html",
        {"request": request, "book": new_book}
    )

@app.delete("/books/{book_id}")
async def delete_book(
    request: Request,
    book_id: int,
    session: Session = Depends(get_session)
):
    """Delete a book (HTMX endpoint)"""
    try:
        user = get_current_user(request, session)
    except HTTPException:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    # TODO: Find and delete book
    book = session.get(Book, book_id)
    if not book or book.user_id != user.id:
        return HTMLResponse(content="Not found", status_code=404)
    
    session.delete(book)
    session.commit()
    
    # Return empty response (HTMX will remove the element)
    return HTMLResponse(content="")

@app.post("/logout")
async def logout(request: Request):
    """Handle user logout"""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)