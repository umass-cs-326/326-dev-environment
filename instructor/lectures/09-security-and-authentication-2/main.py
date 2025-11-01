"""
FastAPI Authentication Demo - Main Application

This is the main entry point for our authentication demo application.
It brings together all the separated modules to create a complete FastAPI application.

This modular structure makes the code much easier to understand and maintain:
- app/core/config.py: All configuration settings
- app/models/user.py: Data models (Pydantic schemas)
- app/db/database.py: Database operations and user storage
- app/core/auth.py: Authentication logic and JWT handling
- app/core/dependencies.py: FastAPI authentication dependencies
- app/api/routes.py: API endpoint definitions
- main.py: Application setup and orchestration

Key concepts:
- Modular architecture and separation of concerns
- FastAPI application factory pattern
- Router inclusion for organizing endpoints
"""

from fastapi import FastAPI

from app.core.config import APP_TITLE, APP_DESCRIPTION
from app.api.routes import router


# =============================================================================
# APPLICATION SETUP
# =============================================================================

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This function sets up the FastAPI app with all necessary configuration
    and includes all the routes from our routes module.
    
    Returns:
        Configured FastAPI application instance
    """
    # Create the FastAPI application with metadata
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version="1.0.0",
        docs_url="/docs",  # Swagger UI at /docs
        redoc_url="/redoc"  # ReDoc documentation at /redoc
    )
    
    # Include all routes from the routes module
    app.include_router(router, prefix="", tags=["authentication"])
    
    return app


# Create the application instance
app = create_app()


# =============================================================================
# APPLICATION EVENTS
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Run when the application starts up.
    
    This is where you would typically:
    - Initialize database connections
    - Load configuration
    - Set up logging
    - Perform health checks
    """
    print("Authentication Demo API is starting up...")
    print("Visit /docs for interactive API documentation")
    print("Test user: username='johndoe', password='secret'")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run when the application shuts down.
    
    This is where you would typically:
    - Close database connections
    - Clean up resources
    - Save state if needed
    """
    print("Authentication Demo API is shutting down...")


# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        Welcome message and basic API information
    """
    return {
        "message": "Welcome to the FastAPI Authentication Demo!",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "login": "POST /token",
            "user_profile": "GET /users/me",
            "user_items": "GET /users/me/items/",
            "public_info": "GET /public/info"
        },
        "test_credentials": {
            "username": "johndoe",
            "password": "secret"
        }
    }


# =============================================================================
# DEVELOPMENT SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the development server
    # In production, you would use a proper ASGI server like Gunicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )