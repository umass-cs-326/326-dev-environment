# FastAPI Authentication - Functions and Data Structures

To view these images, make sure you have the [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) VS Code extension installed.

## Function and Data Structure Flow

```mermaid
graph TB
    %% Data Structures
    DB[(fake_users_db)]
    TOKEN[Token]
    TOKENDATA[TokenData]
    USER[User]
    USERINDB[UserInDB]
    
    %% Helper Functions
    VERIFY[verify_password]
    HASH[get_password_hash]
    GETUSER[get_user]
    AUTH[authenticate_user]
    CREATETOKEN[create_access_token]
    
    %% Dependency Functions
    GETCURRENT[get_current_user]
    GETACTIVE[get_current_active_user]
    
    %% Route Functions
    LOGIN[login_for_access_token]
    USERME[read_users_me]
    ITEMS[read_own_items]
    
    %% Function Dependencies
    DB --> GETUSER
    VERIFY --> AUTH
    GETUSER --> AUTH
    GETUSER --> GETCURRENT
    GETCURRENT --> GETACTIVE
    
    %% Route Dependencies
    AUTH --> LOGIN
    CREATETOKEN --> LOGIN
    GETACTIVE --> USERME
    GETACTIVE --> ITEMS
    
    %% Data Structure Relationships
    USER --> USERINDB
    
    %% Function Data Usage
    HASH -.-> USERINDB
    VERIFY -.-> USERINDB
    CREATETOKEN -.-> TOKEN
    GETCURRENT -.-> TOKENDATA
    LOGIN -.-> TOKEN
    USERME -.-> USER
    
    %% Styling
    classDef dataClass fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef funcClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef routeClass fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef depClass fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class DB,TOKEN,TOKENDATA,USER,USERINDB dataClass
    class VERIFY,HASH,GETUSER,AUTH,CREATETOKEN funcClass
    class LOGIN,USERME,ITEMS routeClass
    class GETCURRENT,GETACTIVE depClass
```

## Data Model Diagram

```mermaid
erDiagram
    fake_users_db {
        string username PK
        string full_name
        string email
        string hashed_password
        boolean disabled
    }
    
    Token {
        string access_token
        string token_type
    }
    
    TokenData {
        string username "Optional"
    }
    
    User {
        string username
        string email "Optional"
        string full_name "Optional"
        boolean disabled "Optional"
    }
    
    UserInDB {
        string username
        string email "Optional"
        string full_name "Optional"
        boolean disabled "Optional"
        string hashed_password
    }
    
    %% Relationships
    fake_users_db ||--|| UserInDB : "maps to"
    User ||--|| UserInDB : "extends"
    User ||--o| Token : "generates"
    TokenData ||--|| User : "references"
```

## Pydantic Model Class Diagram

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
    }
    
    class Token {
        +access_token: str
        +token_type: str
    }
    
    class TokenData {
        +username: Optional[str] = None
    }
    
    class User {
        +username: str
        +email: Optional[str] = None
        +full_name: Optional[str] = None
        +disabled: Optional[bool] = None
    }
    
    class UserInDB {
        +hashed_password: str
    }
    
    class fake_users_db {
        <<dict>>
        +johndoe: dict
    }
    
    BaseModel <|-- Token
    BaseModel <|-- TokenData
    BaseModel <|-- User
    User <|-- UserInDB
    fake_users_db ..> UserInDB : instantiates
    
    note for User "Base user model for API responses"
    note for UserInDB "User model with password hash for database storage"
    note for Token "JWT token response model"
    note for TokenData "Token payload data model"
```
