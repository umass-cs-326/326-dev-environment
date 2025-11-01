import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

BASE_SOURCE_DIR = '/autograder/source'
SOURCE_DIR = f'{BASE_SOURCE_DIR}/hw2'
BASE_SUBMISSION_DIR = '/autograder/submission'
SUBMISSION_DIR = f'{BASE_SUBMISSION_DIR}/hw2'


LOG_PATH = f"{SOURCE_DIR}/app.log"

# Ensure results directory exists
os.makedirs('/autograder/results', exist_ok=True)

# Add submission directory to Python path
sys.path.insert(0, SUBMISSION_DIR)


# Results structure for Gradescope
results = {
    "stdout_visibility": "visible",
    "output": "",
    "tests": [],
    "score": 0.0,
    "max_score": 0.0,
}


def replace_dsn(root: str = ".") -> tuple[int, int]:
    """
    Recursively find and replace the exact DSN string in all Python files.

    Returns (files_modified, total_replacements).
    """
    old = "postgresql+psycopg://app:app@dev_pg:5432/db"
    new = "postgresql+psycopg://app:app@localhost:5432/db"
    skip_dirs = {".git", "__pycache__", ".venv", "venv",
                 "node_modules", ".mypy_cache", ".ruff_cache"}

    files_modified = 0
    total_replacements = 0

    for path in Path(root).rglob("*.py"):
        if any(part in skip_dirs for part in path.parts):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")

        if old in text:
            occurrences = text.count(old)
            path.write_text(text.replace(old, new), encoding="utf-8")
            files_modified += 1
            total_replacements += occurrences

    return files_modified, total_replacements


def log(s: str):
    results["output"] += s


def log_app_log():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        data = f.read()
        log(data)


def add_test_result(name, max_score, score, output=""):
    """Add a test result to the results dictionary"""
    results["tests"].append({
        "name": name,
        "max_score": max_score,
        "score": score,
        "output": output
    })
    results["score"] += score
    results["max_score"] += max_score


log_file = open(LOG_PATH, "ab", buffering=0)


def start_fastapi_server():
    """Start the FastAPI server in the background"""
    try:
        log_file.write(b"[launcher] uvicorn starting...\n")

        print("Trying to start FastAPI Server.")
        process = subprocess.Popen(
            ["python3", "-m", "uvicorn", "main:app",
                "--host", "0.0.0.0", "--port", "8000",
                "--access-log", "--log-level", "warning",
                "--use-colors"],
            cwd=SOURCE_DIR,
            stdout=log_file,
            stderr=subprocess.STDOUT
        )
        # Wait for server to start
        time.sleep(5)
        print("FastAPI Server Started.")
        return process
    except Exception as e:
        print(f'{str(e)}')
        return None


# Patch in the correct DSN
replace_dsn()

# Test 1: Check file structure
try:
    hw2_path = Path(SOURCE_DIR)
    if not hw2_path.exists():
        add_test_result("File Structure", 5, 0, "hw2 directory not found")
    elif not (hw2_path / "models.py").exists() or not (hw2_path / "main.py").exists():
        add_test_result("File Structure", 5, 0,
                        "Required files (models.py and/or main.py) not found")
    else:
        add_test_result("File Structure", 5, 5, "All required files present")
except Exception as e:
    add_test_result("File Structure", 5, 0, str(e))

# Test 2: Import models
try:
    from models import Author, Book
    add_test_result("Model Imports", 10, 10, "Models imported successfully")

    # Verify Author has required fields
    author_fields = Author.__annotations__
    if 'id' in author_fields and 'name' in author_fields and 'email' in author_fields:
        add_test_result("Author Model Fields", 5, 5,
                        "Author model has all required fields")
    else:
        add_test_result("Author Model Fields", 5, 0,
                        "Author model missing required fields")

    # Verify Book has required fields
    book_fields = Book.__annotations__
    if all(field in book_fields for field in ['id', 'title', 'year', 'author_id']):
        add_test_result("Book Model Fields", 5, 5,
                        "Book model has all required fields")
    else:
        add_test_result("Book Model Fields", 5, 0,
                        "Book model missing required fields")

except Exception as e:
    add_test_result("Model Imports", 10, 0,
                    f"Failed to import models: {str(e)}")
    add_test_result("Author Model Fields", 5, 0,
                    "Could not verify - import failed")
    add_test_result("Book Model Fields", 5, 0,
                    "Could not verify - import failed")

# Start FastAPI server
server_process = start_fastapi_server()
if server_process is None:
    add_test_result("Server Startup", 5, 0, "Failed to start FastAPI server")
    BASE_URL = None
else:
    add_test_result("Server Startup", 5, 5,
                    "FastAPI server started successfully")
    BASE_URL = "http://127.0.0.1:8000"

# Run API endpoint tests
if BASE_URL:
    try:
        with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
            # Test Task 2: Author CRUD operations

            # POST /authors/
            response = client.post(
                "/authors/", json={"name": "Test Author", "email": "test@example.com"})
            if response.status_code == 200 or response.status_code == 201:
                add_test_result("POST /authors/", 5, 5,
                                "Author created successfully")
                author_id = response.json().get("id")
            else:
                add_test_result("POST /authors/", 5, 0,
                                f"Failed with status {response.status_code}")
                author_id = None

            # GET /authors/
            response = client.get("/authors/")
            if response.status_code == 200 and len(response.json()) > 0:
                add_test_result("GET /authors/", 5, 5,
                                "Authors retrieved successfully")
            else:
                add_test_result("GET /authors/", 5, 0,
                                "Failed to retrieve authors")

            # GET /authors/{id}
            if author_id:
                response = client.get(f"/authors/{author_id}")
                if response.status_code == 200:
                    add_test_result(
                        "GET /authors/{id}", 5, 5, "Author retrieved by ID")
                else:
                    add_test_result(
                        "GET /authors/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "GET /authors/{id}", 5, 0, "Skipped - no author created")

            # PATCH /authors/{id}
            if author_id:
                response = client.patch(
                    f"/authors/{author_id}", json={"name": "Updated Author"})
                if response.status_code == 200:
                    add_test_result(
                        "PATCH /authors/{id}", 5, 5, "Author updated successfully")
                else:
                    add_test_result(
                        "PATCH /authors/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "PATCH /authors/{id}", 5, 0, "Skipped - no author created")

            # DELETE /authors/{id} - test later after book tests

            # Test Task 3: Book CRUD operations

            # POST /books/
            if author_id:
                response = client.post(
                    "/books/", json={"title": "Test Book", "year": 2020, "author_id": author_id})
                if response.status_code == 200 or response.status_code == 201:
                    add_test_result("POST /books/", 8, 8,
                                    "Book created successfully")
                    book_id = response.json().get("id")
                else:
                    add_test_result("POST /books/", 8, 0,
                                    f"Failed with status {response.status_code}")
                    book_id = None
            else:
                add_test_result("POST /books/", 8, 0,
                                "Skipped - no author to associate with")
                book_id = None

            # GET /books/
            response = client.get("/books/")
            if response.status_code == 200:
                add_test_result("GET /books/", 7, 7,
                                "Books retrieved successfully")
            else:
                add_test_result("GET /books/", 7, 0,
                                "Failed to retrieve books")

            # GET /books/{id}
            if book_id:
                response = client.get(f"/books/{book_id}")
                if response.status_code == 200:
                    add_test_result(
                        "GET /books/{id}", 5, 5, "Book retrieved by ID")
                else:
                    add_test_result(
                        "GET /books/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result("GET /books/{id}",
                                5, 0, "Skipped - no book created")

            # GET /books/by-author/{author_id}
            if author_id:
                response = client.get(f"/books/by-author/{author_id}")
                if response.status_code == 200:
                    add_test_result(
                        "GET /books/by-author/{id}", 5, 5, "Books by author retrieved")
                else:
                    add_test_result(
                        "GET /books/by-author/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "GET /books/by-author/{id}", 5, 0, "Skipped - no author")

            # PATCH /books/{id}
            if book_id:
                response = client.patch(
                    f"/books/{book_id}", json={"title": "Updated Book"})
                if response.status_code == 200:
                    add_test_result(
                        "PATCH /books/{id}", 5, 5, "Book updated successfully")
                else:
                    add_test_result(
                        "PATCH /books/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "PATCH /books/{id}", 5, 0, "Skipped - no book created")

            # DELETE /books/{id}
            if book_id:
                response = client.delete(f"/books/{book_id}")
                if response.status_code == 200 or response.status_code == 204:
                    add_test_result(
                        "DELETE /books/{id}", 5, 5, "Book deleted successfully")
                else:
                    add_test_result(
                        "DELETE /books/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "DELETE /books/{id}", 5, 0, "Skipped - no book created")

            # Now test DELETE /authors/{id}
            if author_id:
                response = client.delete(f"/authors/{author_id}")
                if response.status_code == 200 or response.status_code == 204:
                    add_test_result(
                        "DELETE /authors/{id}", 5, 5, "Author deleted successfully")
                else:
                    add_test_result(
                        "DELETE /authors/{id}", 5, 0, f"Failed with status {response.status_code}")
            else:
                add_test_result(
                    "DELETE /authors/{id}", 5, 0, "Skipped - no author created")

            # Test Task 4: Reset endpoint
            response = client.delete("/reset/")
            if response.status_code == 200 or response.status_code == 204:
                add_test_result("DELETE /reset/", 10, 10,
                                "Reset endpoint works correctly")
            else:
                add_test_result("DELETE /reset/", 10, 0,
                                f"Failed with status {response.status_code} - {response.text}")

    except Exception as e:
        add_test_result("API Tests", 20, 0, f"API testing failed: {str(e)}")
else:
    # Skip all API tests if server didn't start
    add_test_result("API Tests - Skipped", 75, 0,
                    "Server failed to start, all API tests skipped. " +
                    "Please make sure your connection string to the database " +
                    "is postgresql+psycopg://app:app@localhost:5432/db.")
    # postgresql+psycopg: // app: app@localhost: 5432/db


# Clean up
if server_process:
    log_file.close()
    server_process.terminate()
    server_process.wait()

# Add the output of the server to help students debug.
log_app_log()

# Write results
with open('/autograder/results/results.json', 'w') as f:
    json.dump(results, f, indent=2)
