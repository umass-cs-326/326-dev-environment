Great — here’s the **annotated live coding script**. I’ve added *talking points* for you to use while typing, so the class flows as a guided narrative.

---

# Lecture 05 Live Coding – Annotated Script

---

### Part 1 – Start Flat App

```python
from fastapi import FastAPI
app = FastAPI()
todos = []

@app.post("/todos")
def create_todo(item: str):
    todos.append(item)
    return {"todos": todos}

@app.get("/todos")
def list_todos():
    return todos
```

**Talking Points**

* “Here’s the simplest Todo app in one file. A global list holds the todos.”
* “This is fine for demos, but what happens when our app grows?”
* “We’ll start introducing *dependencies* to cleanly share state.”

---

### Part 2 – Add `get_db` Dependency

```python
from fastapi import Depends

def get_db():
    return {"todos": todos}

@app.get("/todos")
def list_todos(db = Depends(get_db)):
    return db["todos"]
```

**Talking Points**

* “I wrote a little function `get_db()` that returns the database — right now just a dict.”
* “Instead of reaching into a global variable, the route declares what it *depends on*.”
* “FastAPI calls `get_db()` for us and injects the result.”
* “This pattern lets us swap the DB later without changing all the routes.”

---

### Part 3 – Add `get_current_user` Dependency

```python
from fastapi import Depends, HTTPException

def get_current_user():
    # pretend authentication
    return {"username": "alice"}

@app.get("/me")
def read_me(user = Depends(get_current_user)):
    return user
```

**Talking Points**

* “Dependencies aren’t just for data — they can handle authentication, logging, or config.”
* “Here’s a stub that pretends to authenticate a user.”
* “Any route that needs the current user can declare it in the signature.”
* “Notice how clean this is: no copy-paste of auth logic.”

---

### Part 4 – Combine Dependencies

```python
@app.get("/secure-todos")
def secure_todos(
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    return {"user": user, "todos": db["todos"]}
```

**Talking Points**

* “Dependencies can be combined. This route needs both the user and the database.”
* “FastAPI resolves all dependencies before calling the route.”
* “Dependencies can even depend on other dependencies — they’re composable.”

---

### Part 5 – Refactor into Folders

Create structure:

```
app/
  main.py
  routers/todos.py
  models/todo.py
  dependencies/db.py
  dependencies/auth.py
```

**main.py**

```python
from fastapi import FastAPI
from app.routers import todos

app = FastAPI()
app.include_router(todos.router)
```

**routers/todos.py**

```python
from fastapi import APIRouter, Depends
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/todos")

@router.get("/")
def list_todos(db = Depends(get_db), user = Depends(get_current_user)):
    return {"user": user, "todos": db["todos"]}
```

**Talking Points**

* “We’re now refactoring into a project structure you’ll use in homework.”
* “`routers/` holds the endpoints, `dependencies/` holds shared logic.”
* “Notice: the router imports the dependencies — clean separation of concerns.”
* “This is the step from a toy app to a maintainable application.”

---

### Part 6 – Test and Recap

* Run:

  ```bash
  uvicorn app.main:app --reload
  ```
* Visit `/todos/` → see todos with user
* Visit `/me` → see the stub user

**Talking Points**

* “Now our app is modular, testable, and ready to grow.”
* “Next lecture, we’ll connect to a real database. But the structure won’t change — just the dependency.”

---

Do you also want me to prepare a **student coding exercise** (e.g., “write your own dependency for request timing/logging”) so they can practice during or after the lecture?
